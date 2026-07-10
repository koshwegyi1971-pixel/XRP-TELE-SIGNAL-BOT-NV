import requests
import logging

logger = logging.getLogger(__name__)

class FASentimentService:
    @staticmethod
    def get_sentiment():
        """
        Fetches Fear & Greed Index from Alternative.me (common for crypto).
        """
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
        Fetches basic XRP fundamentals from CoinGecko.
        """
        try:
            # Using CoinGecko public API
            url = "https://api.coingecko.com/api/v3/coins/ripple?localization=false&tickers=false&market_data=true&community_data=false&developer_data=true&sparkline=false"
            response = requests.get(url, timeout=10)
            data = response.json()
            
            market_cap_rank = data.get('market_cap_rank', 'N/A')
            fdv = data['market_data'].get('fully_diluted_valuation', {}).get('usd', 'N/A')
            dev_score = data.get('developer_score', 'N/A')
            
            return f"- Market Cap Rank: {market_cap_rank}\n- Fully Diluted Valuation: ${fdv}\n- Developer Score: {dev_score}"
        except Exception as e:
            logger.error(f"Error fetching fundamentals: {e}")
            return "Fundamental data currently unavailable."
