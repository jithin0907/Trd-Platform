from models.trade import Trade

trade = Trade(
    strategy="EMA Pullback",
    symbol="EURUSD",
    timeframe="M15",
    direction="BUY",
    entry_price=1.1050,
    stop_loss=1.1020,
    take_profit=1.1110,
    lot_size=0.10
)

print(trade)