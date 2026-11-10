from datetime import UTC, datetime
from decimal import Decimal

from agentic_system_for_trading.collector import Collector
from agentic_system_for_trading.models import MarketSnapshot
from agentic_system_for_trading.retry import RetryPolicy


def make_snapshot() -> MarketSnapshot:
    return MarketSnapshot(
        symbol="BTC/USDT",
        source="fake",
        captured_at=datetime(2026, 11, 8, 19, 38, 18, tzinfo=UTC),
        bid=Decimal("75889.2"),
        ask=Decimal("75889.21"),
        low_24h=Decimal("75571.08"),
        high_24h=Decimal("76200.0"),
        volume_24h=Decimal("5226.22363"),
        change_pct_24h=Decimal("0.147"),
    )


class FakeSource:
    def __init__(self, snapshot):
        self._snapshot = snapshot

    def fetch_snapshot(self, symbol):
        return self._snapshot

    def is_available(self):
        return True


class InMemorySink:
    def __init__(self):
        self.saved = []

    def save(self, snapshot):
        self.saved.append(snapshot)


def test_collect_saves_snapshot_from_source_to_sink():
    snapshot = make_snapshot()
    sink = InMemorySink()
    collector = Collector(
        source=FakeSource(snapshot),
        sink=sink,
        retry=RetryPolicy(sleep=lambda seconds: None),
    )

    collector.collect("BTC/USDT")

    assert sink.saved == [snapshot]
