import logging
import httpx
from openai import AsyncOpenAI
from app.config import OPENROUTER_API_KEY, OPENROUTER_MODEL

logger = logging.getLogger(__name__)

class AIService:
    def __init__(self):
        # Explicitly initialize with a clean httpx client to avoid 'proxies' argument issues
        # that can occur in some environments (like Render) due to automatic proxy detection.
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
                    {"role": "system", "content": "You are an institutional-grade crypto trading expert. Provide concise, data-driven market analysis and DCA recommendations for XRP."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=800
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error calling OpenRouter: {e}")
            return f"Error generating AI analysis: {str(e)}"

    def _build_prompt(self, data: dict) -> str:
        return f"""
Analyze the following XRP market data and provide a summary report:

Current Price: ${data.get('price', 'N/A')}
Market Regime: {data.get('regime', 'N/A')}
Sentiment: {data.get('sentiment', 'N/A')}

Technical Indicators (1H):
- RSI: {data.get('indicators_1h', {}).get('rsi', 'N/A')}
- MACD: {data.get('indicators_1h', {}).get('macd', 'N/A')}
- Trend: {data.get('indicators_1h', {}).get('trend', 'N/A')}

Technical Indicators (4H):
- RSI: {data.get('indicators_4h', {}).get('rsi', 'N/A')}
- Trend: {data.get('indicators_4h', {}).get('trend', 'N/A')}

Fundamental Highlights:
{data.get('fundamentals', 'N/A')}

Requirements:
1. Summarize current market condition.
2. Provide a clear recommendation (ACCUMULATE, HOLD, or REDUCE).
3. Identify specific DCA buy/sell price zones.
4. Keep it professional and concise.
"""
