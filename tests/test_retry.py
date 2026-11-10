import pytest

from agentic_system_for_trading.retry import RetryPolicy


def make_flaky(failures, error, result="ok"):
    calls = {"n": 0}

    def func():
        calls["n"] += 1
        if calls["n"] <= failures:
            raise error
        return result

    return func


def test_returns_result_without_sleeping_when_first_call_succeeds():
    sleeps = []
    policy = RetryPolicy(
        max_attempts=3,
        base_delay_s=1.0,
        retry_on=(ConnectionError, TimeoutError),
        sleep=sleeps.append,
    )

    result = policy.call(lambda: "ok")

    assert result == "ok"
    assert sleeps == []


def test_returns_result_on_second_attempt():
    sleeps = []

    flaky = make_flaky(1, ConnectionError("down"))

    policy = RetryPolicy(
        max_attempts=3,
        base_delay_s=1.0,
        retry_on=(ConnectionError, TimeoutError),
        sleep=sleeps.append,
    )

    result = policy.call(flaky)

    assert result == "ok"
    assert sleeps == [1.0]


def test_sleeps_increase_with_each_attempt():
    sleeps = []

    flaky = make_flaky(3, ConnectionError("down"))

    policy = RetryPolicy(
        max_attempts=4,
        base_delay_s=1.0,
        retry_on=(ConnectionError, TimeoutError),
        sleep=sleeps.append,
    )

    result = policy.call(flaky)

    assert result == "ok"
    assert sleeps == [1.0, 2.0, 4.0]


def test_raises_last_error_when_all_attempts_failed():
    sleeps = []

    flaky = make_flaky(3, ConnectionError("down"))

    with pytest.raises(ConnectionError):
        policy = RetryPolicy(
            max_attempts=3,
            base_delay_s=1.0,
            retry_on=(ConnectionError, TimeoutError),
            sleep=sleeps.append,
        )
        policy.call(flaky)

    assert sleeps == [1.0, 2.0]
