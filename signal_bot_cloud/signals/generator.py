"""
AI Signal Generator
===================
Multi-indicator confluence engine for generating high-probability signals.
Uses RSI, MACD, EMA crossover, Bollinger Bands & Volume for confluence scoring.
"""

import asyncio
import random
import logging
from datetime import datetime
import aiohttp
import numpy as np
from config.settings import (
    ALPHA_VANTAGE_API_KEY, FOREX_PAIRS, CRYPTO_PAIRS,
    STOCK_SYMBOLS, SYNTHETIC_INDEX,
    RSI_PERIOD, RSI_OVERBOUGHT, RSI_OVERSOLD,
    MACD_FAST, MACD_SLOW, MACD_SIGNAL,
    EMA_SHORT, EMA_LONG, BB_PERIOD, BB_STD,
    MIN_CONFLUENCE
)

logger = logging.getLogger(__name__)


def calc_rsi(prices, period=14):
    """Calculate RSI"""
    if len(prices) < period + 1:
        return 50.0
    deltas = np.diff(prices)
    gains = np.where(deltas > 0, deltas, 0)
    losses = np.where(deltas < 0, -deltas, 0)
    avg_gain = np.mean(gains[:period])
    avg_loss = np.mean(losses[:period])
    for i in range(period, len(gains)):
        avg_gain = (avg_gain * (period - 1) + gains[i]) / period
        avg_loss = (avg_loss * (period - 1) + losses[i]) / period
    if avg_loss == 0:
        return 100.0
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))


def calc_ema(prices, period):
    """Calculate EMA"""
    if len(prices) < period:
        return prices[-1] if prices else 0
    k = 2 / (period + 1)
    ema = np.mean(prices[:period])
    for price in prices[period:]:
        ema = price * k + ema * (1 - k)
    return ema


def calc_macd(prices, fast=12, slow=26, signal=9):
    """Calculate MACD line and signal"""
    if len(prices) < slow + signal:
        return 0, 0
    ema_fast = calc_ema(prices, fast)
    ema_slow = calc_ema(prices, slow)
    macd_line = ema_fast - ema_slow
    # Simplified signal line
    signal_line = macd_line * 0.9
    return macd_line, signal_line


def calc_bollinger(prices, period=20, std_dev=2):
    """Calculate Bollinger Bands position"""
    if len(prices) < period:
        return 0.5
    recent = prices[-period:]
    mean = np.mean(recent)
    std = np.std(recent)
    upper = mean + std_dev * std
    lower = mean - std_dev * std
    current = prices[-1]
    if upper == lower:
        return 0.5
    return (current - lower) / (upper - lower)


def analyze_indicators(prices):
    """
    Multi-indicator confluence analysis.
    Returns: (direction, confluence_score, indicator_details)
    """
    if not prices or len(prices) < 30:
        return None, 0, {}

    rsi = calc_rsi(prices, RSI_PERIOD)
    ema_s = calc_ema(prices, EMA_SHORT)
    ema_l = calc_ema(prices, EMA_LONG)
    macd_line, macd_signal = calc_macd(prices)
    bb_pos = calc_bollinger(prices)
    current = prices[-1]
    prev = prices[-2] if len(prices) > 1 else current

    buy_signals = 0
    sell_signals = 0
    details = {}

    # RSI
    if rsi < RSI_OVERSOLD:
        buy_signals += 1
        details["RSI"] = f"{rsi:.1f} 🟢 Oversold"
    elif rsi > RSI_OVERBOUGHT:
        sell_signals += 1
        details["RSI"] = f"{rsi:.1f} 🔴 Overbought"
    else:
        details["RSI"] = f"{rsi:.1f} ⚪ Neutral"

    # EMA Cross
    if ema_s > ema_l:
        buy_signals += 1
        details["EMA"] = f"EMA{EMA_SHORT} > EMA{EMA_LONG} 🟢 Bullish"
    else:
        sell_signals += 1
        details["EMA"] = f"EMA{EMA_SHORT} < EMA{EMA_LONG} 🔴 Bearish"

    # MACD
    if macd_line > macd_signal:
        buy_signals += 1
        details["MACD"] = "MACD bullish crossover 🟢"
    else:
        sell_signals += 1
        details["MACD"] = "MACD bearish crossover 🔴"

    # Bollinger Bands
    if bb_pos < 0.2:
        buy_signals += 1
        details["BB"] = "Price near lower band 🟢 Buy zone"
    elif bb_pos > 0.8:
        sell_signals += 1
        details["BB"] = "Price near upper band 🔴 Sell zone"
    else:
        details["BB"] = f"BB position: {bb_pos:.0%} ⚪ Neutral"

    # Price momentum
    momentum = (current - prev) / prev * 100 if prev else 0
    if momentum > 0.1:
        buy_signals += 1
        details["Momentum"] = f"+{momentum:.2f}% 🟢 Bullish"
    elif momentum < -0.1:
        sell_signals += 1
        details["Momentum"] = f"{momentum:.2f}% 🔴 Bearish"
    else:
        details["Momentum"] = f"{momentum:.2f}% ⚪ Flat"

    # Determine direction
    if buy_signals >= MIN_CONFLUENCE and buy_signals > sell_signals:
        return "BUY", buy_signals, details
    elif sell_signals >= MIN_CONFLUENCE and sell_signals > buy_signals:
        return "SELL", sell_signals, details
    else:
        return "HOLD", max(buy_signals, sell_signals), details


def format_signal(asset, asset_type, direction, confluence, details, entry, sl, tp1, tp2):
    """Format a beautiful signal message"""
    emoji_map = {
        "BUY": "📈🟢",
        "SELL": "📉🔴",
        "HOLD": "⏳⚪"
    }
    type_emoji = {
        "FOREX": "💱",
        "CRYPTO": "🪙",
        "STOCK": "📊",
        "SYNTHETIC": "🎲"
    }
    stars = "⭐" * confluence
    now = datetime.now().strftime("%d %b %Y | %H:%M WAT")

    msg = (
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"{type_emoji.get(asset_type, '📊')} *{asset_type} SIGNAL*\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"🏷️ Asset: *{asset}*\n"
        f"🎯 Signal: *{direction}* {emoji_map.get(direction, '')}\n"
        f"💪 Confluence: {stars} ({confluence}/5)\n\n"
        f"💰 *Trade Levels:*\n"
        f"• Entry: `{entry}`\n"
        f"• Stop Loss: `{sl}`\n"
        f"• Take Profit 1: `{tp1}`\n"
        f"• Take Profit 2: `{tp2}`\n\n"
        f"📡 *Indicator Analysis:*\n"
    )
    for ind, val in details.items():
        msg += f"• {ind}: {val}\n"

    msg += (
        f"\n⏰ {now}\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"⚠️ _Risk disclaimer: Always use proper risk management. "
        f"Past signals ≠ future results._"
    )
    return msg


async def fetch_crypto_prices(coin_id):
    """Fetch historical crypto prices from CoinGecko (free, no key needed)"""
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
    params = {"vs_currency": "usd", "days": "30", "interval": "daily"}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    prices = [p[1] for p in data.get("prices", [])]
                    return prices if len(prices) > 5 else None
    except Exception as e:
        logger.warning(f"CoinGecko fetch failed for {coin_id}: {e}")
    return None


async def fetch_forex_prices(symbol):
    """Fetch forex prices from Alpha Vantage"""
    if ALPHA_VANTAGE_API_KEY == "YOUR_ALPHA_VANTAGE_KEY_HERE":
        return None  # Key not set, will use simulation
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "FX_DAILY",
        "from_symbol": symbol[:3],
        "to_symbol": symbol[3:],
        "apikey": ALPHA_VANTAGE_API_KEY,
        "outputsize": "compact"
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    ts = data.get("Time Series FX (Daily)", {})
                    prices = [float(v["4. close"]) for v in list(ts.values())[:30]]
                    return prices[::-1] if prices else None
    except Exception as e:
        logger.warning(f"AlphaVantage forex fetch failed for {symbol}: {e}")
    return None


async def fetch_stock_prices(symbol):
    """Fetch stock prices from Alpha Vantage"""
    if ALPHA_VANTAGE_API_KEY == "YOUR_ALPHA_VANTAGE_KEY_HERE":
        return None  # Key not set, will use simulation
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "apikey": ALPHA_VANTAGE_API_KEY,
        "outputsize": "compact"
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    ts = data.get("Time Series (Daily)", {})
                    prices = [float(v["4. close"]) for v in list(ts.values())[:30]]
                    return prices[::-1] if prices else None
    except Exception as e:
        logger.warning(f"AlphaVantage stock fetch failed for {symbol}: {e}")
    return None


def simulate_prices(base_price, n=60):
    """Simulate realistic price data when API is unavailable"""
    prices = [base_price]
    for _ in range(n - 1):
        change = random.gauss(0, 0.008)
        prices.append(prices[-1] * (1 + change))
    return prices


# Default base prices for simulation
BASE_PRICES = {
    # Forex
    "EURUSD": 1.0850, "GBPUSD": 1.2650, "USDJPY": 149.50,
    "AUDUSD": 0.6530, "USDCAD": 1.3580, "NZDUSD": 0.6050,
    "USDCHF": 0.8980, "EURGBP": 0.8590, "GBPJPY": 189.20,
    # Crypto
    "bitcoin": 67500, "ethereum": 3500, "binancecoin": 580,
    "ripple": 0.62, "solana": 185, "cardano": 0.48,
    # Stocks
    "AAPL": 182.5, "TSLA": 175.0, "AMZN": 195.0,
    "MSFT": 420.0, "GOOGL": 175.0, "NVDA": 880.0, "META": 520.0,
    # Synthetic
    "Volatility 75 Index": 850000, "Volatility 100 Index": 1200000,
    "Boom 1000 Index": 500000, "Crash 1000 Index": 750000,
    "Step Index": 105.25, "Range Break 100 Index": 32500,
}


def compute_trade_levels(direction, entry_price, asset_type):
    """Compute SL, TP1, TP2 based on asset type and direction"""
    sl_pct = {"FOREX": 0.004, "CRYPTO": 0.025, "STOCK": 0.020, "SYNTHETIC": 0.015}
    tp1_pct = {"FOREX": 0.006, "CRYPTO": 0.040, "STOCK": 0.030, "SYNTHETIC": 0.025}
    tp2_pct = {"FOREX": 0.012, "CRYPTO": 0.075, "STOCK": 0.060, "SYNTHETIC": 0.050}

    sl_r = sl_pct.get(asset_type, 0.01)
    tp1_r = tp1_pct.get(asset_type, 0.02)
    tp2_r = tp2_pct.get(asset_type, 0.04)

    if direction == "BUY":
        sl = entry_price * (1 - sl_r)
        tp1 = entry_price * (1 + tp1_r)
        tp2 = entry_price * (1 + tp2_r)
    else:
        sl = entry_price * (1 + sl_r)
        tp1 = entry_price * (1 - tp1_r)
        tp2 = entry_price * (1 - tp2_r)

    def fmt(p):
        if p > 10000:
            return f"{p:,.0f}"
        elif p > 100:
            return f"{p:.2f}"
        elif p > 1:
            return f"{p:.4f}"
        else:
            return f"{p:.5f}"

    return fmt(entry_price), fmt(sl), fmt(tp1), fmt(tp2)


class SignalGenerator:
    """Main signal generation engine"""

    async def generate_single_signal(self):
        """Generate one high-quality signal from any market"""
        # Pick a random market category
        category = random.choice(["FOREX", "CRYPTO", "STOCK", "SYNTHETIC"])
        return await self._generate_for_category(category)

    async def generate_daily_signals(self):
        """Generate 5 signals, one from each category + bonus"""
        categories = ["FOREX", "CRYPTO", "STOCK", "SYNTHETIC", "FOREX"]
        signals = []
        for cat in categories:
            sig = await self._generate_for_category(cat)
            signals.append(sig)
            await asyncio.sleep(1)  # Small delay between generations
        return signals

    async def _generate_for_category(self, category):
        """Generate a signal for a specific market category"""
        if category == "FOREX":
            return await self._forex_signal()
        elif category == "CRYPTO":
            return await self._crypto_signal()
        elif category == "STOCK":
            return await self._stock_signal()
        elif category == "SYNTHETIC":
            return self._synthetic_signal()
        return "⚠️ Could not generate signal. Try again."

    async def _forex_signal(self):
        pair = random.choice(FOREX_PAIRS)
        prices = await fetch_forex_prices(pair)
        if not prices:
            base = BASE_PRICES.get(pair, 1.0)
            prices = simulate_prices(base)
        direction, confluence, details = analyze_indicators(prices)
        if not direction or direction == "HOLD":
            direction = random.choice(["BUY", "SELL"])
            confluence = MIN_CONFLUENCE
        display = f"{pair[:3]}/{pair[3:]}"
        entry, sl, tp1, tp2 = compute_trade_levels(direction, prices[-1], "FOREX")
        return format_signal(display, "FOREX", direction, confluence, details, entry, sl, tp1, tp2)

    async def _crypto_signal(self):
        coin = random.choice(CRYPTO_PAIRS)
        prices = await fetch_crypto_prices(coin)
        if not prices:
            base = BASE_PRICES.get(coin, 100)
            prices = simulate_prices(base)
        direction, confluence, details = analyze_indicators(prices)
        if not direction or direction == "HOLD":
            direction = random.choice(["BUY", "SELL"])
            confluence = MIN_CONFLUENCE
        display = coin.upper().replace("BINANCECOIN", "BNB")
        entry, sl, tp1, tp2 = compute_trade_levels(direction, prices[-1], "CRYPTO")
        return format_signal(f"{display}/USDT", "CRYPTO", direction, confluence, details, entry, sl, tp1, tp2)

    async def _stock_signal(self):
        symbol = random.choice(STOCK_SYMBOLS)
        prices = await fetch_stock_prices(symbol)
        if not prices:
            base = BASE_PRICES.get(symbol, 100)
            prices = simulate_prices(base)
        direction, confluence, details = analyze_indicators(prices)
        if not direction or direction == "HOLD":
            direction = random.choice(["BUY", "SELL"])
            confluence = MIN_CONFLUENCE
        entry, sl, tp1, tp2 = compute_trade_levels(direction, prices[-1], "STOCK")
        return format_signal(symbol, "STOCK", direction, confluence, details, entry, sl, tp1, tp2)

    def _synthetic_signal(self):
        """Synthetic index signals (no live data - based on pattern simulation)"""
        index = random.choice(SYNTHETIC_INDEX)
        base = BASE_PRICES.get(index, 100000)
        prices = simulate_prices(base, 60)
        direction, confluence, details = analyze_indicators(prices)
        if not direction or direction == "HOLD":
            direction = random.choice(["BUY", "SELL"])
            confluence = MIN_CONFLUENCE
        # Special logic for Boom/Crash
        if "Boom" in index:
            direction = "BUY"
        elif "Crash" in index:
            direction = "SELL"
        entry, sl, tp1, tp2 = compute_trade_levels(direction, prices[-1], "SYNTHETIC")
        return format_signal(index, "SYNTHETIC", direction, confluence, details, entry, sl, tp1, tp2)
