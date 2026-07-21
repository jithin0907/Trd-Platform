from providers.data_provider import DataProvider
from strategies.crt.structure import Structure


provider = DataProvider()

provider.connect()

df = provider.get_market_data(
    symbol="EURUSD",
    timeframe="M5",
    bars=300
)

swings = Structure.detect_swings(
    df,
    lookback=5
)

last_high = Structure.get_last_swing_high(swings)

last_low = Structure.get_last_swing_low(swings)

bos = Structure.detect_bos(
    df,
    last_high,
    last_low
)




print("\n========== LAST SWINGS ==========\n")

if last_high:

    print(
        "Last Swing High :",
        last_high["time"],
        round(last_high["price"], 5)
    )

if last_low:

    print(
        "Last Swing Low  :",
        last_low["time"],
        round(last_low["price"], 5)
    )

print("\n========== BOS ==========\n")

print("BOS       :", bos["bos"])
print("Direction :", bos["direction"])
print("Level     :", bos["level"])
print("Time      :", bos["time"])