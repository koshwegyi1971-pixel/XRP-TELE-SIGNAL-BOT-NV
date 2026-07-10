import logging
from telegram import Bot
from telegram.constants import ParseMode

logger = logging.getLogger(__name__)

class TelegramService:
    def __init__(self, token, chat_id):
        self.bot = Bot(token=token)
        self.chat_id = chat_id

    async def send_message(self, text, parse_mode=ParseMode.MARKDOWN):
        try:
            await self.bot.send_message(
                chat_id=self.chat_id,
                text=text,
                parse_mode=parse_mode,
                disable_web_page_preview=True
            )
        except Exception as e:
            logger.error(f"Error sending Telegram message: {e}")

    async def startup_notification(self):
        msg = "🚀 *XRP TELE SIGNAL BOT NV* is now online!\n\nMonitoring XRP for DCA opportunities with AI-powered insights."
        await self.send_message(msg)
