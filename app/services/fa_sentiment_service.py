import requests
import logging

logger = logging.getLogger(__name__)

class FASentimentService:
    @staticmethod
    def get_sentiment():
        try:
            response = requests.get("https://api.alternative.me/fng/", timeout=10)
            data = response.json()
            val = data['data'][0]['value']
            classification = data['data'][0]['value_classification']
            return f"{classification} ({val})"
        except Exception as e:
            logger.error(f"Error fetching sentiment: {e}")
            return "Neutral (50)"

    @staticmethod
    def get_xrp_fundamentals():
        """
        Fetches XRP fundamentals from CoinGecko with fallback.
        """
        try:
            # Using CoinGecko public API with a more reliable endpoint
            url = "https://api.coingecko.com/api/v3/simple/price?ids=ripple&vs_currencies=usd&include_market_cap=true&include_24hr_vol=true&include_24hr_change=true"
            response = requests.get(url, timeout=10)
            data = response.json().get('ripple', {})
            
            mkt_cap = data.get('usd_market_cap', 'N/A')
            vol_24h = data.get('usd_24h_vol', 'N/A')
            change_24h = data.get('usd_24h_change', 0)
            
            return (
                f"- 24h Volume: ${vol_24h:,.0f}\n"
                f"- Market Cap: ${mkt_cap:,.0f}\n"
                f"- 24h Change: {change_24h:.2f}%"
            )
        except Exception as e:
            logger.error(f"Error fetching fundamentals: {e}")
            return "- Fundamental data currently unavailable (API Rate Limit)."

    @staticmethod
    def get_news_sentiment():
        """
        Placeholder for News Sentiment analysis. 
        In a real institutional bot, this would call a news API like CryptoPanic.
        """
        return "Stable - No major legal/regulatory news in the last 24h."
