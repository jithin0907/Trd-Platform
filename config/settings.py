# =====================================
# PLATFORM MODE
# =====================================

# BACKTEST
# LIVE

BACKTEST = "BACKTEST"
LIVE = "LIVE"

MODE = BACKTEST

# =====================================
# STRATEGY
# =====================================

# ema_pullback
# crt

STRATEGY = "crt"

# =====================================
# MARKET
# =====================================

SYMBOL = "XAGUSD"

TIMEFRAME = "M5"

# =====================================
# BACKTEST SETTINGS
# =====================================

BARS = 1000

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