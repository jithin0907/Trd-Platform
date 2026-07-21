"""
CRT Strategy Configuration
"""

import MetaTrader5 as mt5

# ============================================
# Higher Timeframe Reference
# ============================================

HTF_TIMEFRAME = "H4"

# ============================================
# Entry Timeframe
# ============================================

ENTRY_TIMEFRAME = "M5"

# ============================================
# Number of HTF candles to download
# ============================================

HTF_BARS = 10

# ============================================
# Stop Loss Buffer
# Added beyond sweep wick
# ============================================

SL_BUFFER_PIPS = 5    # pips

# ============================================
# Take Profit Mode
# MID_RANGE
# OPPOSITE_RANGE
# RR
# ============================================
#P_MODE = "OPPOSITE_RANGE"
TP_MODE = "RR"

# ============================================
# Risk Reward
# Used only when TP_MODE == RR
# ============================================

RISK_REWARD = 3.0

# ============================================
# Session Filter
# Future implementation
# ============================================

SESSION_FILTER = False

# ============================================
# Entry Model
# DIRECT
# MSS
# FVG
# ============================================

ENTRY_MODEL = "DIRECT"

# ============================================
# Trade Time To Live
# Future implementation
# ============================================

TTL_BARS = 10