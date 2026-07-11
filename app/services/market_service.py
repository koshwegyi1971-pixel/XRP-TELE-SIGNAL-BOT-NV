import ccxt
import pandas as pd
import logging
from app.config import EXCHANGE_ID, SYMBOL

logger = logging.getLogger(__name__)

class MarketService:
    def __init__(self):
        exchange_class = getattr(ccxt, EXCHANGE_ID)
        self.exchange = exchange_class({
            'enableRateLimit': True,
        })

    def fetch_ohlcv(self, symbol=SYMBOL, timeframe='1h', limit=300):
        """
        Fetches OHLCV data and returns a pandas DataFrame.
        Increased limit to 300 to ensure enough data for EMA200.
        """
        try:
            # For Kraken, ensure we use the correct symbol format if needed
            # but CCXT usually handles 'XRP/USDT' or 'XRP/USD' well.
            ohlcv = self.exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
            if not ohlcv:
                logger.error(f"No OHLCV data returned for {symbol} on {timeframe}")
                return pd.DataFrame()
                
            df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            
            # Convert columns to numeric to be safe
            for col in ['open', 'high', 'low', 'close', 'volume']:
                df[col] = pd.to_numeric(df[col])
                
            return df
        except Exception as e:
            logger.error(f"Error fetching data from {EXCHANGE_ID}: {e}")
            return pd.DataFrame()

    def get_current_price(self, symbol=SYMBOL):
        try:
            ticker = self.exchange.fetch_ticker(symbol)
            return ticker['last']
        except Exception as e:
            logger.error(f"Error fetching ticker: {e}")
            return None

    def multi_timeframe_data(self, symbol=SYMBOL, timeframes=['15m', '1h', '4h']):
        data = {}
        for tf in timeframes:
            df = self.fetch_ohlcv(symbol, tf)
            if not df.empty:
                data[tf] = df
            else:
                logger.warning(f"Empty data for timeframe {tf}")
        return data
