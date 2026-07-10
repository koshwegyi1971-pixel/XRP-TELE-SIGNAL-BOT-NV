import pandas as pd
import pandas_ta as ta
import logging

logger = logging.getLogger(__name__)

class IndicatorService:
    @staticmethod
    def analyze(df: pd.DataFrame):
        """
        Calculates indicators for the given DataFrame.
        """
        if df.empty:
            return {}

        try:
            # Trend
            df['ema20'] = ta.ema(df['close'], length=20)
            df['ema50'] = ta.ema(df['close'], length=50)
            df['ema200'] = ta.ema(df['close'], length=200)

            # Momentum
            df['rsi'] = ta.rsi(df['close'], length=14)
            macd = ta.macd(df['close'])
            df = pd.concat([df, macd], axis=1)

            # Volatility
            df['atr'] = ta.atr(df['high'], df['low'], df['close'], length=14)
            
            # Trend Strength
            adx = ta.adx(df['high'], df['low'], df['close'], length=14)
            df = pd.concat([df, adx], axis=1)

            latest = df.iloc[-1]
            
            # Determine Trend
            trend = "Sideways"
            if latest['ema20'] > latest['ema50'] > latest['ema200']:
                trend = "Strong Bullish"
            elif latest['ema20'] > latest['ema50']:
                trend = "Bullish"
            elif latest['ema20'] < latest['ema50'] < latest['ema200']:
                trend = "Strong Bearish"
            elif latest['ema20'] < latest['ema50']:
                trend = "Bearish"

            return {
                "price": latest['close'],
                "rsi": latest['rsi'],
                "macd": latest['MACD_12_26_9'],
                "macd_signal": latest['MACDs_12_26_9'],
                "macd_hist": latest['MACDh_12_26_9'],
                "atr": latest['atr'],
                "adx": latest['ADX_14'],
                "ema20": latest['ema20'],
                "ema50": latest['ema50'],
                "ema200": latest['ema200'],
                "trend": trend
            }
        except Exception as e:
            logger.error(f"Error calculating indicators: {e}")
            return {}
