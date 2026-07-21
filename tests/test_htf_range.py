from providers.mt5_provider import MT5Provider
from strategies.crt.htf_range import HTFRangeDetector
from strategies.crt.config import HTF_TIMEFRAME, HTF_BARS

provider = MT5Provider()

# Connect to MT5
if not provider.connect():
    raise Exception("Unable to connect to MT5")

df = provider.get_historical_data(
    symbol="EURUSD",
    timeframe=HTF_TIMEFRAME,
    bars=HTF_BARS
)

htf = HTFRangeDetector.get(df)

print("\n========== HTF RANGE ==========\n")

print("Time  :", htf.time)
print("Open  :", htf.open)
print("High  :", htf.high)
print("Low   :", htf.low)
print("Close :", htf.close)
print("Range :", htf.range)
print("Mid   :", htf.mid)

provider.shutdown()