from models.signal import Signal

signal = Signal(
    strategy="EMA Pullback",
    symbol="EURUSD",
    timeframe="M15",
    signal=True,
    direction="BUY",
    entry=1.1050,
    stop_loss=1.1020,
    take_profit=1.1110,
    confidence=90,
    reasons=[
        "9 EMA > 20 EMA > 50 SMA",
        "Price touched 20 EMA",
        "Bullish candle"
    ]
)

print(signal)