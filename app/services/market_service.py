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
        try:
            ohlcv = self.exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
            if not ohlcv:
                return pd.DataFrame()
            df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            for col in ['open', 'high', 'low', 'close', 'volume']:
                df[col] = pd.to_numeric(df[col])
            return df
        except Exception as e:
            logger.error(f"Error fetching {symbol}: {e}")
            return pd.DataFrame()

    def get_ticker_info(self, symbol=SYMBOL):
        """
        Fetches 24h ticker info directly from the exchange.
        """
        try:
            ticker = self.exchange.fetch_ticker(symbol)
            return {
                "last": ticker['last'],
                "change_24h": ticker['percentage'],
                "volume_24h": ticker['quoteVolume']
            }
        except Exception as e:
            logger.error(f"Error fetching ticker info: {e}")
            return None

    def get_market_context(self):
        xrp_data = self.multi_timeframe_data(SYMBOL, ["1h", "4h"])
        xrp_ticker = self.get_ticker_info(SYMBOL)
        
        btc_symbol = "BTC/USDT" if "USDT" in SYMBOL else "BTC/USD"
        btc_ticker = self.get_ticker_info(btc_symbol)
        
        return {
            "xrp": xrp_data,
            "xrp_ticker": xrp_ticker,
            "btc": btc_ticker
        }

    def multi_timeframe_data(self, symbol=SYMBOL, timeframes=['15m', '1h', '4h']):
        data = {}
        for tf in timeframes:
            df = self.fetch_ohlcv(symbol, tf)
            if not df.empty:
                data[tf] = df
        return data
