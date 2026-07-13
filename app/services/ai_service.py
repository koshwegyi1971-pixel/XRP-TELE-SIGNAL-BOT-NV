import logging
import httpx
from openai import AsyncOpenAI
from app.config import OPENROUTER_API_KEY, OPENROUTER_MODEL

logger = logging.getLogger(__name__)

class AIService:
    def __init__(self):
        # Explicitly initialize with a clean httpx client to avoid 'proxies' argument issues
        http_client = httpx.AsyncClient()
        
        self.client = AsyncOpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=OPENROUTER_API_KEY,
            http_client=http_client
        )

    async def get_market_analysis(self, market_data: dict) -> str:
        """
        Generates market analysis and recommendations using OpenRouter.
        """
        if not OPENROUTER_API_KEY:
            return "AI Analysis unavailable: OPENROUTER_API_KEY not set."

        prompt = self._build_prompt(market_data)
        
        try:
            response = await self.client.chat.completions.create(
                model=OPENROUTER_MODEL,
                messages=[
                    {
                        "role": "system", 
                        "content": (
                            "You are an institutional-grade crypto trading expert. "
                            "Provide a structured, data-driven market report for XRP. "
                            "Use a 'Facts and Figures' style. Use Markdown tables for indicators. "
                            "Keep commentary extremely concise and professional."
                        )
                    },
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=1000
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error calling OpenRouter: {e}")
            return f"Error generating AI analysis: {str(e)}"

    def _build_prompt(self, data: dict) -> str:
        return f"""
Analyze the following XRP market data and generate a structured report:

### MARKET OVERVIEW
- **Price:** ${data.get('price', 'N/A')}
- **Regime:** {data.get('regime', 'N/A')}
- **Sentiment:** {data.get('sentiment', 'N/A')}

### TECHNICAL DATA
| Indicator | 1H Timeframe | 4H Timeframe |
| :--- | :--- | :--- |
| RSI | {data.get('indicators_1h', {}).get('rsi', 'N/A')} | {data.get('indicators_4h', {}).get('rsi', 'N/A')} |
| MACD | {data.get('indicators_1h', {}).get('macd', 'N/A')} | N/A |
| Trend | {data.get('indicators_1h', {}).get('trend', 'N/A')} | {data.get('indicators_4h', {}).get('trend', 'N/A')} |
| EMA 20 | {data.get('indicators_1h', {}).get('ema20', 'N/A')} | N/A |
| EMA 50 | {data.get('indicators_1h', {}).get('ema50', 'N/A')} | N/A |
| EMA 200 | {data.get('indicators_1h', {}).get('ema200', 'N/A')} | N/A |

### FUNDAMENTALS
{data.get('fundamentals', 'N/A')}

### REQUIREMENTS
1. Use a clear header for each section.
2. Use a Markdown table for the Technical Data section.
3. **Recommendation:** Provide one clear action (ACCUMULATE, HOLD, or REDUCE).
4. **DCA Strategy:** List specific Buy/Sell zones with prices.
5. Focus on facts and figures; avoid long paragraphs.
"""
