import asyncio
import logging
from app.config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, CHECK_INTERVAL, SYMBOL
from app.services.market_service import MarketService
from app.services.indicator_service import IndicatorService
from app.services.strategy_service import StrategyService
from app.services.telegram_service import TelegramService
from app.services.health_server import start_health_server

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class XRPBot:
    def __init__(self):
        self.market = MarketService()
        self.strategy = StrategyService()
        self.telegram = TelegramService(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID)

    async def run_analysis(self):
        logger.info("Running 4-hour market analysis...")
        try:
            # 1. Fetch 4-hour data only
            market_context = self.market.get_market_context()
            xrp_data = market_context["xrp"]
            
            if "4h" not in xrp_data:
                logger.error("Insufficient 4-hour market data fetched.")
                return

            # 2. Calculate Indicators for 4-hour timeframe
            indicators_4h = IndicatorService.analyze(xrp_data["4h"])

            # 3. Generate Decision-First Report
            report = await self.strategy.generate_report(indicators_4h, market_context)

            # 4. Send to Telegram
            await self.telegram.send_message(report)
            logger.info("Decision report sent to Telegram.")

        except Exception as e:
            logger.error(f"Error in run_analysis: {e}")
            await self.telegram.send_message(f"⚠️ *Bot Error:* {str(e)}")

    async def start(self):
        start_health_server()
        await self.telegram.startup_notification()
        while True:
            await self.run_analysis()
            logger.info(f"Sleeping for {CHECK_INTERVAL} seconds...")
            await asyncio.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    bot = XRPBot()
    asyncio.run(bot.start())
