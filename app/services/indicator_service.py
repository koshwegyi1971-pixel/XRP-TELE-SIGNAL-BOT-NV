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
        if df is None or df.empty or len(df) < 20:
            logger.warning("Insufficient data for indicator analysis.")
            return {}

        try:
            # Trend
            df['ema20'] = ta.ema(df['close'], length=20)
            df['ema50'] = ta.ema(df['close'], length=50)
            
            # EMA200 needs at least 200 bars
            if len(df) >= 200:
                df['ema200'] = ta.ema(df['close'], length=200)
            else:
                df['ema200'] = None

            # Momentum
            df['rsi'] = ta.rsi(df['close'], length=14)
            macd = ta.macd(df['close'])
            if macd is not None:
                df = pd.concat([df, macd], axis=1)

            # Volatility
            df['atr'] = ta.atr(df['high'], df['low'], df['close'], length=14)
            
            # Trend Strength
            adx = ta.adx(df['high'], df['low'], df['close'], length=14)
            if adx is not None:
                df = pd.concat([df, adx], axis=1)

            # Get the last row that has a price
            latest = df.iloc[-1]
            
            # Determine Trend
            trend = "Sideways"
            ema20 = latest.get('ema20')
            ema50 = latest.get('ema50')
            ema200 = latest.get('ema200')

            if ema20 and ema50:
                if ema200:
                    if ema20 > ema50 > ema200:
                        trend = "Strong Bullish"
                    elif ema20 < ema50 < ema200:
                        trend = "Strong Bearish"
                    elif ema20 > ema50:
                        trend = "Bullish"
                    else:
                        trend = "Bearish"
                else:
                    if ema20 > ema50:
                        trend = "Bullish (Short-term)"
                    else:
                        trend = "Bearish (Short-term)"

            # Safe extraction of indicators with fallbacks
            return {
                "price": round(float(latest['close']), 4),
                "rsi": round(float(latest['rsi']), 2) if not pd.isna(latest.get('rsi')) else "N/A",
                "macd": round(float(latest['MACD_12_26_9']), 6) if not pd.isna(latest.get('MACD_12_26_9')) else "N/A",
                "macd_signal": round(float(latest['MACDs_12_26_9']), 6) if not pd.isna(latest.get('MACDs_12_26_9')) else "N/A",
                "macd_hist": round(float(latest['MACDh_12_26_9']), 6) if not pd.isna(latest.get('MACDh_12_26_9')) else "N/A",
                "atr": round(float(latest['atr']), 6) if not pd.isna(latest.get('atr')) else "N/A",
                "adx": round(float(latest['ADX_14']), 2) if not pd.isna(latest.get('ADX_14')) else "N/A",
                "ema20": round(float(ema20), 4) if ema20 else "N/A",
                "ema50": round(float(ema50), 4) if ema50 else "N/A",
                "ema200": round(float(ema200), 4) if ema200 else "N/A",
                "trend": trend
            }
        except Exception as e:
            logger.error(f"Error calculating indicators: {e}")
            return {"price": round(float(df.iloc[-1]['close']), 4), "trend": "Error in Analysis"}
