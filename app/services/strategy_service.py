import logging
from app.services.ai_service import AIService
from app.services.regime_service import RegimeService
from app.services.fa_sentiment_service import FASentimentService

logger = logging.getLogger(__name__)

class StrategyService:
    def __init__(self):
        self.ai = AIService()
        self.fa_sentiment = FASentimentService()

    async def generate_report(self, indicators_1h, indicators_4h):
        """
        Orchestrates the analysis and generates a final report.
        """
        try:
            # 1. Detect Market Regime
            regime = RegimeService.detect(indicators_1h, indicators_4h)
            
            # 2. Get FA & Sentiment
            sentiment = self.fa_sentiment.get_sentiment()
            fundamentals = self.fa_sentiment.get_xrp_fundamentals()
            
            # 3. Prepare data for AI
            analysis_data = {
                "price": indicators_1h.get('price'),
                "regime": regime,
                "sentiment": sentiment,
                "indicators_1h": indicators_1h,
                "indicators_4h": indicators_4h,
                "fundamentals": fundamentals
            }
            
            # 4. Get AI Analysis
            ai_report = await self.ai.get_market_analysis(analysis_data)
            
            return ai_report
            
        except Exception as e:
            logger.error(f"Error generating strategy report: {e}")
            return f"Error generating strategy report: {str(e)}"
