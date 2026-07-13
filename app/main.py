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
        logger.info("Running advanced market analysis...")
        try:
            # 1. Fetch data for XRP and BTC
            market_context = self.market.get_market_context()
            xrp_data = market_context["xrp"]
            btc_context = market_context["btc"]
            
            if "1h" not in xrp_data or "4h" not in xrp_data:
                logger.error("Insufficient market data fetched.")
                return

            # 2. Calculate Advanced Indicators
            indicators_1h = IndicatorService.analyze(xrp_data["1h"])
            indicators_4h = IndicatorService.analyze(xrp_data["4h"])

            # 3. Generate Report via Strategy Service (Institutional Grade)
            report = await self.strategy.generate_report(indicators_1h, indicators_4h, btc_context)

            # 4. Send to Telegram
            await self.telegram.send_message(report)
            logger.info("Institutional report sent to Telegram.")

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
