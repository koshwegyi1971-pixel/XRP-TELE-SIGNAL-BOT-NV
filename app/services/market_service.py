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

    def get_market_context(self):
        """
        Fetches data for both XRP and BTC to provide market context.
        """
        xrp_data = self.multi_timeframe_data(SYMBOL, ["1h", "4h"])
        
        # Fetch BTC for correlation (usually BTC/USDT or BTC/USD)
        btc_symbol = "BTC/USDT" if "USDT" in SYMBOL else "BTC/USD"
        btc_1h = self.fetch_ohlcv(btc_symbol, "1h", limit=100)
        
        btc_price = btc_1h.iloc[-1]['close'] if not btc_1h.empty else None
        btc_change = ((btc_1h.iloc[-1]['close'] / btc_1h.iloc[0]['close']) - 1) * 100 if not btc_1h.empty else 0
        
        return {
            "xrp": xrp_data,
            "btc": {
                "price": btc_price,
                "change_24h": round(btc_change, 2)
            }
        }

    def multi_timeframe_data(self, symbol=SYMBOL, timeframes=['15m', '1h', '4h']):
        data = {}
        for tf in timeframes:
            df = self.fetch_ohlcv(symbol, tf)
            if not df.empty:
                data[tf] = df
        return data
