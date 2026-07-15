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
                            "You are a professional trading desk AI. Generate a DECISION-FIRST report. "
                            "Structure: Executive Summary (Decision + Confidence + Action), Trading Plan (exact zones), Evidence (why). "
                            "Traders need to make decisions in seconds, not read tables. Be direct and actionable."
                        )
                    },
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=1500
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error: {e}")
            return f"Error: {str(e)}"

    def _build_prompt(self, data: dict) -> str:
        btc = data.get('btc_context', {})
        ind = data.get('indicators', {})
        
        return f"""
Generate a DECISION-FIRST trading report for XRP using 4-hour timeframe. Use this exact 3-section structure:

## 1. EXECUTIVE SUMMARY
- **Decision:** (ACCUMULATE / HOLD / REDUCE)
- **Confidence:** (HIGH / MEDIUM / LOW)
- **Action:** (1-2 sentence directive for traders)

## 2. TRADING PLAN
- **Buy Zone:** $X.XX - $X.XX (Entry prices)
- **Stop Loss:** $X.XX (Hard stop)
- **Take Profit:** $X.XX (Exit target)
- **Position Size:** (% of capital based on risk)
- **Risk/Reward Ratio:** (e.g., 1:2)

## 3. EVIDENCE (4-Hour Timeframe)
Explain WHY the decision was made using this data:

**Market Context:**
- XRP Price: ${data.get('price', 'N/A')}
- BTC Context: ${btc.get('price', 'N/A')} ({btc.get('change_24h', 0)}% 24h)
- Regime: {data.get('regime', 'N/A')}
- Sentiment: {data.get('sentiment', 'N/A')}

**Technical Analysis (4H):**
- Trend: {ind.get('trend', 'N/A')}
- RSI: {ind.get('rsi', 'N/A')} (Oversold <30, Overbought >70)
- Volume Ratio: {ind.get('volume_ratio', 'N/A')}x (>1.0 = strong)
- BB Status: {ind.get('bb_status', 'N/A')}
- ADX: {ind.get('adx', 'N/A')} (>25 = trending)

**Market Structure:**
- Pivot: {ind.get('pivot', 'N/A')} | R1: {ind.get('r1', 'N/A')} | S1: {ind.get('s1', 'N/A')}

**Fundamentals & News:**
{data.get('fundamentals', 'N/A')}
- News: {data.get('news', 'N/A')}

**AI Scoring:**
- Confluence Score: (List which indicators align)
- Risk Assessment: (What could go wrong?)

---
CRITICAL RULES:
1. Decision MUST come first, not buried in analysis.
2. Confidence level MUST be explicit (HIGH/MEDIUM/LOW).
3. Trading Plan MUST be immediately executable (exact prices, no ranges except Buy Zone).
4. Evidence MUST justify the decision, not replace it.
5. Keep each section concise—traders scan, not read.
"""
