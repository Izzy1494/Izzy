# 🤖 AI Signal Bot — Complete Setup Guide

## Overview
This bot sends **5 trading signals daily** via Telegram for:
- 💱 Forex | 🪙 Crypto | 📈 Stocks | 🎲 Synthetic Index

---

## ✅ STEP-BY-STEP SETUP

### STEP 1 — Install Python
Download Python 3.10+ from https://python.org
Make sure to check **"Add Python to PATH"** during install.

---

### STEP 2 — Create Your Telegram Bot (FREE)
1. Open Telegram and search for **@BotFather**
2. Send: `/newbot`
3. Follow prompts → give your bot a name (e.g. `My Signal Bot`)
4. BotFather will give you a **token** like:
   ```
   7123456789:AAHdq...your_token_here
   ```
5. Copy this token — you'll need it in Step 4.

---

### STEP 3 — Get Your Telegram Chat ID
1. Search for **@userinfobot** on Telegram
2. Send it `/start`
3. It will reply with your **Chat ID** (a number like `123456789`)
4. Copy this number.

---

### STEP 4 — Configure the Bot
Open the file: `config/settings.py`

Replace these lines:
```python
TELEGRAM_BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN_HERE"
CHAT_ID = "YOUR_TELEGRAM_CHAT_ID_HERE"
ALPHA_VANTAGE_API_KEY = "YOUR_ALPHA_VANTAGE_KEY_HERE"
```

With your actual values:
```python
TELEGRAM_BOT_TOKEN = "7123456789:AAHdq..."
CHAT_ID = "123456789"
ALPHA_VANTAGE_API_KEY = "ABC123XYZ"  # See Step 5
```

---

### STEP 5 — Get Free Alpha Vantage API Key (for Forex + Stocks)
1. Visit: https://www.alphavantage.co/support/#api-key
2. Sign up free → get your key instantly
3. Paste it in `config/settings.py`

> ⚠️ Free tier: 25 requests/day (plenty for our 5 signals)
> CoinGecko (crypto) needs no key.

---

### STEP 6 — Install Dependencies
Open a terminal/command prompt in the `signal_bot` folder and run:
```bash
pip install -r requirements.txt
```

---

### STEP 7 — Run the Bot!
```bash
python bot.py
```

You should see:
```
✅ Bot is live! Listening for commands...
⏰ Scheduler started. 5 signals/day scheduled (WAT timezone).
```

Now open Telegram, find your bot, and send `/start` 🎉

---

## 📅 Signal Schedule (West Africa Time)
| # | Time | Market |
|---|------|--------|
| 1 | 06:00 AM | Forex |
| 2 | 09:00 AM | Crypto |
| 3 | 12:00 PM | Stocks |
| 4 | 03:00 PM | Synthetic Index |
| 5 | 06:00 PM | Forex |

---

## 🤖 Bot Commands
| Command | Action |
|---------|--------|
| `/start` | Start bot + show menu |
| `/signal` | Get an instant signal NOW |
| `/status` | Check bot health |
| `/markets` | See all tracked assets |
| `/help` | Show help menu |

---

## 🖥️ Running 24/7 (Optional)

### On Windows — Use Task Scheduler
1. Create a `.bat` file:
   ```bat
   @echo off
   cd C:\path\to\signal_bot
   python bot.py
   ```
2. Set it to run on startup in Windows Task Scheduler.

### On Linux/Mac — Use a systemd service or screen:
```bash
screen -S signalbot
python bot.py
# Press Ctrl+A then D to detach
```

### On a VPS (Recommended for 24/7)
Use any cheap VPS (DigitalOcean, Contabo, etc.) and run:
```bash
nohup python bot.py &
```

---

## ⚠️ Important Disclaimer
> Trading signals are generated using technical analysis indicators.
> They do **not** guarantee profits. Always use proper risk management,
> never risk more than 1-2% per trade, and do your own research.

---

## 📁 Project Structure
```
signal_bot/
├── bot.py              ← Main bot file (run this)
├── requirements.txt    ← Dependencies
├── README.md           ← This guide
├── config/
│   └── settings.py     ← YOUR CREDENTIALS & SETTINGS
└── signals/
    ├── generator.py    ← AI signal engine (RSI, MACD, EMA, BB)
    └── scheduler.py    ← 5 daily signal scheduler
```
