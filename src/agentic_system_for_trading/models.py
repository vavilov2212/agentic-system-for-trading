from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass(frozen=True)
class MarketSnapshot:
    symbol: str
    source: str
    captured_at: datetime
    bid: Decimal
    ask: Decimal
    low_24h: Decimal
    high_24h: Decimal
    volume_24h: Decimal
    change_pct_24h: Decimal

    def __post_init__(self) -> None:
        if self.captured_at.tzinfo is None:
            raise ValueError("captured_at must be timezone-aware (UTC)")
