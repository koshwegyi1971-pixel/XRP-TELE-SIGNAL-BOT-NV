import logging

logger = logging.getLogger(__name__)

class RegimeService:
    @staticmethod
    def detect(indicators_1h: dict, indicators_4h: dict) -> str:
        """
        Detects the current market regime based on TA indicators.
        """
        try:
            adx = indicators_1h.get('adx', 0)
            rsi = indicators_1h.get('rsi', 50)
            trend_1h = indicators_1h.get('trend', 'Sideways')
            trend_4h = indicators_4h.get('trend', 'Sideways')

            # Regime Logic
            if adx > 25:
                if trend_1h == "Strong Bullish" and trend_4h in ["Strong Bullish", "Bullish"]:
                    return "Trending Bull (Strong)"
                elif trend_1h == "Strong Bearish" and trend_4h in ["Strong Bearish", "Bearish"]:
                    return "Trending Bear (Strong)"
                elif "Bullish" in trend_1h:
                    return "Trending Bull"
                elif "Bearish" in trend_1h:
                    return "Trending Bear"
            
            if 40 < rsi < 60 and adx < 20:
                return "Sideways / Consolidation"
            
            if rsi > 70:
                return "Overbought / Potential Reversal"
            if rsi < 30:
                return "Oversold / Potential Reversal"

            return "Mixed / Volatile"
        except Exception as e:
            logger.error(f"Error detecting regime: {e}")
            return "Unknown"
