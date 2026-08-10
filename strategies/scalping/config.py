"""
====================================================
Scalping Strategy Configuration
====================================================
Strategy  : Grid Scalping
Symbol    : XAGUSD
Timeframe : M1
====================================================
"""


class ScalpingConfig:
    """
    Scalping Strategy Configuration
    """

    # ==================================================
    # SYMBOL SETTINGS
    # ==================================================

    SYMBOL = "XAGUSD"
    TIMEFRAME = "M1"

    # ==================================================
    # TRADE SETTINGS
    # ==================================================

    BASE_LOT_SIZE = 0.02

    MAGIC_NUMBER = 20260801

    MAX_SLIPPAGE = 10

    # ==================================================
    # GRID SETTINGS
    # ==================================================

    ENABLE_GRID = True

    GRID_SPACING_PRICE = 0.15

    MAX_GRID_ORDERS = 4

    # ==================================================
    # BASKET SETTINGS
    # ==================================================

    TARGET_PROFIT_USD = 8.00

    CLOSE_ALL_ON_TARGET = True

    # ==================================================
    # SAFETY SETTINGS
    # ==================================================

    MAX_SPREAD = 0.05

    ENABLE_TRADING_HOURS = False

    TRADING_START = "00:00"

    TRADING_END = "23:59"

    # ==================================================
    # PAUSE SETTINGS
    # ==================================================

    ENABLE_MANUAL_PAUSE = True

    START_PAUSED = False

    # ==================================================
    # EMERGENCY SETTINGS
    # ==================================================

    ENABLE_EMERGENCY_KILL = True

    # ==================================================
    # LOGGING
    # ==================================================

    PRINT_SIGNALS = True

    PRINT_GRID = True

    PRINT_BASKET = True

    PRINT_ORDERS = True