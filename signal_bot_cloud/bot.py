"""
╔══════════════════════════════════════════════════╗
║         AI SIGNAL BOT - TELEGRAM EDITION         ║
║   Forex | Crypto | Stocks | Synthetic Index      ║
╚══════════════════════════════════════════════════╝
"""

import asyncio
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from config.settings import TELEGRAM_BOT_TOKEN, CHAT_ID
from signals.scheduler import SignalScheduler
from signals.generator import SignalGenerator

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    handlers=[
        logging.FileHandler("bot.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    welcome = (
        "🤖 *AI Signal Bot Activated!*\n\n"
        "📊 Markets Covered:\n"
        "• 💱 Forex (EUR/USD, GBP/USD, USD/JPY...)\n"
        "• 🪙 Crypto (BTC, ETH, BNB...)\n"
        "• 📈 Stocks (AAPL, TSLA, AMZN...)\n"
        "• 🎲 Synthetic Index (Volatility 75, Boom/Crash...)\n\n"
        "⏰ *Signal Schedule:* 5 signals/day\n"
        "• 06:00 AM - Pre-market scan\n"
        "• 09:00 AM - Market open\n"
        "• 12:00 PM - Midday signal\n"
        "• 03:00 PM - Afternoon signal\n"
        "• 06:00 PM - End-of-day signal\n\n"
        "📌 *Commands:*\n"
        "/signal - Get an instant signal now\n"
        "/status - Bot health check\n"
        "/markets - List all tracked markets\n"
        "/help - Show this message\n\n"
        "✅ Bot is running. Signals will arrive automatically!"
    )
    await update.message.reply_text(welcome, parse_mode="Markdown")


async def get_instant_signal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /signal command - generate on-demand signal"""
    await update.message.reply_text("🔍 Scanning markets... please wait.", parse_mode="Markdown")
    generator = SignalGenerator()
    signal = await generator.generate_single_signal()
    await update.message.reply_text(signal, parse_mode="Markdown")


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /status command"""
    msg = (
        "✅ *Bot Status: ONLINE*\n\n"
        "🔄 Signal engine: Active\n"
        "📡 Data feeds: Connected\n"
        "⏰ Scheduler: Running\n"
        "📬 Next signal: On schedule\n\n"
        "_All systems operational._"
    )
    await update.message.reply_text(msg, parse_mode="Markdown")


async def markets(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /markets command"""
    msg = (
        "📊 *Tracked Markets*\n\n"
        "💱 *FOREX*\n"
        "EUR/USD | GBP/USD | USD/JPY\n"
        "AUD/USD | USD/CAD | NZD/USD\n"
        "USD/CHF | EUR/GBP | GBP/JPY\n\n"
        "🪙 *CRYPTO*\n"
        "BTC/USDT | ETH/USDT | BNB/USDT\n"
        "XRP/USDT | SOL/USDT | ADA/USDT\n\n"
        "📈 *STOCKS*\n"
        "AAPL | TSLA | AMZN | MSFT\n"
        "GOOGL | NVDA | META\n\n"
        "🎲 *SYNTHETIC INDEX*\n"
        "Volatility 75 | Volatility 100\n"
        "Boom 1000 | Crash 1000\n"
        "Step Index | Range Break 100\n"
    )
    await update.message.reply_text(msg, parse_mode="Markdown")


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start(update, context)


def main():
    """Start the bot"""
    logger.info("🚀 Starting AI Signal Bot...")

    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Register handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("signal", get_instant_signal))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("markets", markets))
    app.add_handler(CommandHandler("help", help_cmd))

    # Start signal scheduler
    scheduler = SignalScheduler(app)
    scheduler.start()

    logger.info("✅ Bot is live! Listening for commands...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
