from datetime import UTC, datetime
from decimal import Decimal

import ccxt

from agentic_system_for_trading.models import MarketSnapshot


class BinanceSource:
    def __init__(self) -> None:
        self._exchange = ccxt.binance()

    def is_available(self) -> bool:
        try:
            self._exchange.fetch_time()
        except ccxt.BaseError:
            return False
        return True

    def fetch_snapshot(self, symbol: str) -> MarketSnapshot:
        ticker = self._exchange.fetch_ticker(symbol)
        return ticker_to_snapshot(ticker, source="binance")


def _to_decimal(ticker: dict, key: str) -> Decimal:
    value = ticker.get(key)
    if value is None:
        raise ValueError(f"ticker has no value for '{key}'")
    return Decimal(str(value))


def ticker_to_snapshot(ticker: dict, source: str) -> MarketSnapshot:
    timestamp_ms = ticker.get("timestamp")
    if timestamp_ms is None:
        raise ValueError("ticker has no timestamp")
    return MarketSnapshot(
        symbol=ticker["symbol"],
        source=source,
        captured_at=datetime.fromtimestamp(timestamp_ms / 1000, tz=UTC),
        bid=_to_decimal(ticker, "bid"),
        ask=_to_decimal(ticker, "ask"),
        low_24h=_to_decimal(ticker, "low"),
        high_24h=_to_decimal(ticker, "high"),
        volume_24h=_to_decimal(ticker, "baseVolume"),
        change_pct_24h=_to_decimal(ticker, "percentage"),
    )
