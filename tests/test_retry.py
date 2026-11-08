from agentic_system_for_trading.retry import RetryPolicy


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
    policy = RetryPolicy(
        max_attempts=3,
        base_delay_s=1.0,
        retry_on=(ConnectionError, TimeoutError),
        sleep=sleeps.append(sleeps[sleeps.count() + 1]),
    )

    result = policy.call(lambda: "error")

    assert result == "ok"
    assert sleeps == [1.0]
