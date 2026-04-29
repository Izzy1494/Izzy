"""
Signal Scheduler
================
Sends 5 signals at configured times each day using APScheduler.
"""

import logging
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import pytz
from config.settings import SIGNAL_TIMES, TIMEZONE, CHAT_ID
from signals.generator import SignalGenerator

logger = logging.getLogger(__name__)


class SignalScheduler:
    def __init__(self, app):
        self.app = app
        self.scheduler = AsyncIOScheduler(timezone=pytz.timezone(TIMEZONE))
        self.generator = SignalGenerator()
        self._setup_jobs()

    def _setup_jobs(self):
        """Register all 5 daily signal jobs"""
        for i, time_str in enumerate(SIGNAL_TIMES):
            hour, minute = map(int, time_str.split(":"))
            # Rotate through market types: Forex, Crypto, Stock, Synthetic, Forex
            categories = ["FOREX", "CRYPTO", "STOCK", "SYNTHETIC", "FOREX"]
            category = categories[i % len(categories)]

            self.scheduler.add_job(
                self._send_scheduled_signal,
                CronTrigger(hour=hour, minute=minute),
                args=[category, i + 1],
                id=f"signal_{i+1}",
                name=f"Signal #{i+1} - {category} at {time_str}",
                replace_existing=True
            )
            logger.info(f"📅 Scheduled: Signal #{i+1} ({category}) at {time_str} WAT")

    async def _send_scheduled_signal(self, category, signal_num):
        """Generate and send a scheduled signal"""
        try:
            logger.info(f"⚡ Generating Signal #{signal_num} [{category}]...")
            header = (
                f"🔔 *SCHEDULED SIGNAL #{signal_num}/5*\n"
                f"━━━━━━━━━━━━━━━━━━━━━━\n\n"
            )
            signal = await self.generator._generate_for_category(category)
            full_message = header + signal

            await self.app.bot.send_message(
                chat_id=CHAT_ID,
                text=full_message,
                parse_mode="Markdown"
            )
            logger.info(f"✅ Signal #{signal_num} sent successfully.")
        except Exception as e:
            logger.error(f"❌ Failed to send Signal #{signal_num}: {e}")

    def start(self):
        """Start the scheduler"""
        self.scheduler.start()
        logger.info(f"⏰ Scheduler started. 5 signals/day scheduled (WAT timezone).")

    def stop(self):
        """Stop the scheduler"""
        self.scheduler.shutdown()
        logger.info("⏹️ Scheduler stopped.")
