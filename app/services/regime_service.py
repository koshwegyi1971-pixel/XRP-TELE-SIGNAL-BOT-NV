import logging

logger = logging.getLogger(__name__)

class RegimeService:
    @staticmethod
    def detect_4h(indicators_4h: dict) -> str:
        """
        Detects market regime based on 4-hour indicators only.
        """
        try:
            adx = indicators_4h.get('adx', 0)
            rsi = indicators_4h.get('rsi', 50)
            trend = indicators_4h.get('trend', 'Sideways')

            # Regime Logic
            if adx > 25:
                if "Bullish" in trend:
                    return "Trending Bull (Strong)"
                elif "Bearish" in trend:
                    return "Trending Bear (Strong)"
            
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
