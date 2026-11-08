from datetime import UTC, datetime
from decimal import Decimal
from unittest.mock import Mock

import pytest
from agentic_system_for_trading.sources.ccxt_source import (
    CcxtSource,
    ticker_to_snapshot,
)

SAMPLE_TICKER = {
    "symbol": "BTC/USDT",
    "timestamp": 1761400000000,
    "bid": 67000.1,
    "ask": 67000.2,
    "low": 65000.0,
    "high": 68000.0,
    "baseVolume": 1234.5,
    "percentage": 1.2,
}


def test_ticker_to_snapshot_maps_fields():
    snapshot = ticker_to_snapshot(SAMPLE_TICKER, source="binance")
    assert snapshot.symbol == SAMPLE_TICKER["symbol"]
    assert snapshot.source == "binance"
    assert snapshot.captured_at == datetime(2025, 10, 25, 13, 46, 40, tzinfo=UTC)
    assert snapshot.bid == Decimal(str(SAMPLE_TICKER["bid"]))
    assert snapshot.low_24h == Decimal(str(SAMPLE_TICKER["low"]))
    assert snapshot.volume_24h == Decimal(str(SAMPLE_TICKER["baseVolume"]))
    assert snapshot.high_24h == Decimal(str(SAMPLE_TICKER["high"]))
    assert snapshot.change_pct_24h == Decimal(str(SAMPLE_TICKER["percentage"]))


def test_ticker_to_snapshot_rejects_missing_bid():
    ticker = {**SAMPLE_TICKER, "bid": None}

    with pytest.raises(ValueError, match="bid"):
        ticker_to_snapshot(ticker, source="binance")


# def test_fetch_snapshot_raises_error():
#     ticker = CcxtSource("binance").fetch_snapshot(symbol=SAMPLE_TICKER["symbol"])


def test_fetch_snapshot_with_mock():
    exchange = Mock()
    exchange.fetch_ticker.return_value = SAMPLE_TICKER

    snapshot = CcxtSource("binance", exchange=exchange).fetch_snapshot("BTC/USDT")

    exchange.fetch_ticker.assert_called_once_with("BTC/USDT")
    assert snapshot.symbol == "BTC/USDT"
