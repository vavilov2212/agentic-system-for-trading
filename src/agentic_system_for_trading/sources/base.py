from typing import Protocol

from agentic_system_for_trading.models import MarketSnapshot


class DataSource(Protocol):
    def fetch_snapshot(self, symbol: str) -> MarketSnapshot: ...

    def is_available(self) -> bool: ...
