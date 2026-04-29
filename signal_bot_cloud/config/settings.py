"""
Configuration Settings — Cloud Ready
======================================
Reads credentials from environment variables (for Railway, Render, VPS).
Set these in your hosting dashboard — never hardcode secrets in code.
"""

import os

# ── Telegram ──────────────────────────────────────────────────────────────────
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
CHAT_ID            = os.environ.get("CHAT_ID",            "")

# ── Alpha Vantage (Forex + Stocks) ────────────────────────────────────────────
ALPHA_VANTAGE_API_KEY = os.environ.get("ALPHA_VANTAGE_API_KEY", "")

# ── Signal Schedule (WAT = UTC+1, 5 signals/day) ─────────────────────────────
SIGNAL_TIMES = ["06:00", "09:00", "12:00", "15:00", "18:00"]
TIMEZONE     = "Africa/Lagos"

# ── Tracked Assets ────────────────────────────────────────────────────────────
FOREX_PAIRS = [
    "EURUSD", "GBPUSD", "USDJPY",
    "AUDUSD", "USDCAD", "NZDUSD",
    "USDCHF", "EURGBP", "GBPJPY",
]

CRYPTO_PAIRS = [
    "bitcoin", "ethereum", "binancecoin",
    "ripple", "solana", "cardano",
]

STOCK_SYMBOLS = [
    "AAPL", "TSLA", "AMZN",
    "MSFT", "GOOGL", "NVDA", "META",
]

SYNTHETIC_INDEX = [
    "Volatility 75 Index",
    "Volatility 100 Index",
    "Boom 1000 Index",
    "Crash 1000 Index",
    "Step Index",
    "Range Break 100 Index",
]

# ── Technical Analysis Parameters ─────────────────────────────────────────────
RSI_PERIOD     = 14
RSI_OVERBOUGHT = 70
RSI_OVERSOLD   = 30
MACD_FAST      = 12
MACD_SLOW      = 26
MACD_SIGNAL    = 9
EMA_SHORT      = 9
EMA_LONG       = 21
BB_PERIOD      = 20
BB_STD         = 2
MIN_CONFLUENCE = 3
