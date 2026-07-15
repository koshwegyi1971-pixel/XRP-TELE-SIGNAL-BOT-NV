import logging
from telegram import Bot, Update
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram.constants import ParseMode

logger = logging.getLogger(__name__)

class TelegramService:
    def __init__(self, token, chat_id):
        self.bot = Bot(token=token)
        self.chat_id = chat_id
        self.app = Application.builder().token(token).build()
        self.report_callback = None

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
        msg = (
            "🚀 *XRP TELE SIGNAL BOT NV* is now online!\n\n"
            "📊 Monitoring XRP with AI-powered 4-hour analysis.\n\n"
            "Commands:\n"
            "/report - Get instant market analysis\n"
            "/help - Show available commands"
        )
        await self.send_message(msg)

    async def handle_report_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /report command to generate on-demand analysis."""
        try:
            await context.bot.send_message(
                chat_id=self.chat_id,
                text="⏳ Analyzing XRP market... Please wait.",
                parse_mode=ParseMode.MARKDOWN
            )
            
            # Call the report generation callback if set
            if self.report_callback:
                report = await self.report_callback()
                await self.send_message(report)
            else:
                await self.send_message("❌ Report generation not available yet.")
        except Exception as e:
            logger.error(f"Error handling report command: {e}")
            await self.send_message(f"❌ Error: {str(e)}")

    async def handle_help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command."""
        help_text = (
            "📖 *XRP TELE SIGNAL BOT NV - Commands*\n\n"
            "/report - Get instant XRP market analysis (4H)\n"
            "/help - Show this help message\n\n"
            "Automatic Reports: Hourly analysis at the top of each hour.\n"
            "Decision-First Format: Executive Summary → Trading Plan → Evidence"
        )
        await self.send_message(help_text)

    def set_report_callback(self, callback):
        """Set the callback function for on-demand report generation."""
        self.report_callback = callback

    async def start_command_listener(self):
        """Start listening for Telegram commands."""
        self.app.add_handler(CommandHandler("report", self.handle_report_command))
        self.app.add_handler(CommandHandler("help", self.handle_help_command))
        
        logger.info("Telegram command handlers registered.")
        await self.app.initialize()
        await self.app.start()
        await self.app.updater.start_polling()
