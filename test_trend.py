from providers.mt5_provider import MT5Provider
from strategies.ema_pullback.trend import TrendDetector

mt5 = MT5Provider()

if mt5.connect():

    df = mt5.get_historical_data(
        symbol="EURUSD",
        timeframe="M15",
        bars=200
    )

    trend = TrendDetector.detect(df)

    print()

    print("Detected Trend :", trend)

    mt5.shutdown()