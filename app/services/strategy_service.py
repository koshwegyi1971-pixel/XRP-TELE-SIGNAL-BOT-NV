import logging
from app.services.ai_service import AIService
from app.services.regime_service import RegimeService
from app.services.fa_sentiment_service import FASentimentService

logger = logging.getLogger(__name__)

class StrategyService:
    def __init__(self):
        self.ai = AIService()
        self.fa_sentiment = FASentimentService()

    async def generate_report(self, indicators_1h, indicators_4h, market_context):
        """
        Orchestrates the analysis using exchange-direct data.
        """
        try:
            regime = RegimeService.detect(indicators_1h, indicators_4h)
            sentiment = self.fa_sentiment.get_sentiment()
            news = self.fa_sentiment.get_news_sentiment()
            
            # Use ticker info from market_context for reliable fundamentals
            xrp_ticker = market_context.get("xrp_ticker", {})
            btc_ticker = market_context.get("btc", {})
            
            fundamentals = (
                f"- 24h Volume: ${xrp_ticker.get('volume_24h', 0):,.0f}\n"
                f"- 24h Change: {xrp_ticker.get('change_24h', 0):+.2f}%"
            )
            
            analysis_data = {
                "price": indicators_1h.get('price'),
                "regime": regime,
                "sentiment": sentiment,
                "indicators_1h": indicators_1h,
                "indicators_4h": indicators_4h,
                "fundamentals": fundamentals,
                "news": news,
                "btc_context": {
                    "price": btc_ticker.get('last'),
                    "change_24h": btc_ticker.get('change_24h')
                }
            }
            
            ai_report = await self.ai.get_market_analysis(analysis_data)
            return ai_report
            
        except Exception as e:
            logger.error(f"Error: {e}")
            return f"Error: {str(e)}"
