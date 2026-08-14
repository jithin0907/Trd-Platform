# =====================================
# PLATFORM MODE
# =====================================

# BACKTEST
# LIVE
#scalping

BACKTEST = "BACKTEST"
LIVE = "LIVE"

MODE = LIVE



MAX_ENTRY_DEVIATION = 0.025

# =====================================
# STRATEGY
# =====================================

# ema_pullback
# crt
#scalping

STRATEGY = "crt"

# =====================================
# MARKET
# =====================================

SYMBOLS = [
    "XAGUSD",
    "XAUUSD"
]
TIMEFRAME = "M5"

# =====================================
# BACKTEST SETTINGS
# =====================================

BARS = 3000

WARMUP = 100

# =====================================
# LIVE TRADING SETTINGS
# =====================================

LOT_SIZE = 0.01

ONE_TRADE_PER_SYMBOL = True

MAGIC_NUMBER = 10001

MAX_SPREAD = 30

AUTO_RECONNECT = True

# =====================================
# RISK MANAGEMENT
# =====================================

RISK_PERCENT = 1.0

MAX_DAILY_LOSS = 5.0

# =====================================
# LOGGING
# =====================================

LOG_TRADES = True

LOG_SIGNALS = True