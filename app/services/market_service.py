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

    def fetch_ohlcv(self, symbol=SYMBOL, timeframe='1h', limit=100):
        """
        Fetches OHLCV data and returns a pandas DataFrame.
        """
        try:
            ohlcv = self.exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
            df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
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
        return data
