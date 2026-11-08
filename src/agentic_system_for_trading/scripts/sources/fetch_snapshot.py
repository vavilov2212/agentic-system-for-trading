from agentic_system_for_trading.sources.ccxt_source import CcxtSource

try:
    result = CcxtSource("binance").fetch_snapshot("BTC/USDT")
    print("Result: ", result)
except BaseException as e:
    print("Error: ", e)
