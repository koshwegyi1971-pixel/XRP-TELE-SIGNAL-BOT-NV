import logging
import httpx
from openai import AsyncOpenAI
from app.config import OPENROUTER_API_KEY, OPENROUTER_MODEL

logger = logging.getLogger(__name__)

class AIService:
    def __init__(self):
        http_client = httpx.AsyncClient()
        self.client = AsyncOpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=OPENROUTER_API_KEY,
            http_client=http_client
        )

    async def get_market_analysis(self, market_data: dict) -> str:
        if not OPENROUTER_API_KEY:
            return "AI Analysis unavailable."

        prompt = self._build_prompt(market_data)
        
        try:
            response = await self.client.chat.completions.create(
                model=OPENROUTER_MODEL,
                messages=[
                    {
                        "role": "system", 
                        "content": (
                            "You are an institutional-grade crypto trading expert. "
                            "Provide a professional, data-driven market report. "
                            "Always include precise Stop Loss (SL) and Take Profit (TP) levels. "
                            "Focus on risk management and market structure. "
                            "Use Markdown tables and keep it concise."
                        )
                    },
                    {"role": "user", "content": prompt}
                ],
                temperature=0.4,
                max_tokens=1200
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error: {e}")
            return f"Error: {str(e)}"

    def _build_prompt(self, data: dict) -> str:
        btc = data.get('btc_context', {})
        return f"""
Analyze the following XRP market data and generate an institutional report:

### 1. MARKET CONTEXT
- **XRP Price:** ${data.get('price', 'N/A')}
- **BTC Price:** ${btc.get('price', 'N/A')} ({btc.get('change_24h', 0)}% 24h)
- **Market Regime:** {data.get('regime', 'N/A')}
- **Fear & Greed:** {data.get('sentiment', 'N/A')}

### 2. TECHNICAL ANALYSIS (CONFLUENCE)
| Indicator | 1H Timeframe | 4H Timeframe |
| :--- | :--- | :--- |
| Trend | {data.get('indicators_1h', {}).get('trend', 'N/A')} | {data.get('indicators_4h', {}).get('trend', 'N/A')} |
| RSI | {data.get('indicators_1h', {}).get('rsi', 'N/A')} | {data.get('indicators_4h', {}).get('rsi', 'N/A')} |
| Vol. Ratio | {data.get('indicators_1h', {}).get('volume_ratio', 'N/A')}x | N/A |
| BB Status | {data.get('indicators_1h', {}).get('bb_status', 'N/A')} | N/A |
| ATR (Volatility) | {data.get('indicators_1h', {}).get('atr', 'N/A')} | N/A |

### 3. MARKET STRUCTURE (PIVOT LEVELS)
- **Pivot Point:** {data.get('indicators_1h', {}).get('pivot', 'N/A')}
- **Resistance:** R1: {data.get('indicators_1h', {}).get('r1', 'N/A')} | R2: {data.get('indicators_1h', {}).get('r2', 'N/A')}
- **Support:** S1: {data.get('indicators_1h', {}).get('s1', 'N/A')} | S2: {data.get('indicators_1h', {}).get('s2', 'N/A')}

### 4. FUNDAMENTALS & NEWS
{data.get('fundamentals', 'N/A')}
- **News Sentiment:** {data.get('news', 'N/A')}

### INSTRUCTIONS
1. Use Pivot Levels to define precise Entry, Stop Loss (SL), and Take Profit (TP) levels.
2. **Recommendation:** (ACCUMULATE, HOLD, or REDUCE).
3. **DCA Zones:** Provide clear price ranges for entries.
4. **Risk Management:** MUST specify SL and TP levels for the current recommendation.
5. Keep the report clean, using tables and bullet points.
"""
