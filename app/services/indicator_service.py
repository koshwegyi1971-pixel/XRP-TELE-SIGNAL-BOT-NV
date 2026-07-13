import pandas as pd
import pandas_ta as ta
import logging

logger = logging.getLogger(__name__)

class IndicatorService:
    @staticmethod
    def analyze(df: pd.DataFrame):
        if df is None or df.empty or len(df) < 20:
            return {}

        try:
            # 1. Trend
            df['ema20'] = ta.ema(df['close'], length=20)
            df['ema50'] = ta.ema(df['close'], length=50)
            df['ema200'] = ta.ema(df['close'], length=200) if len(df) >= 200 else None

            # 2. Momentum
            df['rsi'] = ta.rsi(df['close'], length=14)
            macd = ta.macd(df['close'])
            if macd is not None:
                df = pd.concat([df, macd], axis=1)

            # 3. Volatility
            df['atr'] = ta.atr(df['high'], df['low'], df['close'], length=14)
            bbands = ta.bbands(df['close'], length=20, std=2)
            if bbands is not None:
                df = pd.concat([df, bbands], axis=1)
            
            # 4. Trend Strength
            adx = ta.adx(df['high'], df['low'], df['close'], length=14)
            if adx is not None:
                df = pd.concat([df, adx], axis=1)

            # 5. Volume Analysis - Using rolling mean for better comparison
            df['v_sma20'] = df['volume'].rolling(window=20).mean()
            df['v_ratio'] = df['volume'] / df['v_sma20']

            # 6. Pivot Points
            prev_row = df.iloc[-2]
            p = (prev_row['high'] + prev_row['low'] + prev_row['close']) / 3
            r1 = (2 * p) - prev_row['low']
            s1 = (2 * p) - prev_row['high']
            r2 = p + (prev_row['high'] - prev_row['low'])
            s2 = p - (prev_row['high'] - prev_row['low'])

            latest = df.iloc[-1]
            
            trend = "Sideways"
            ema20 = latest.get('ema20')
            ema50 = latest.get('ema50')
            ema200 = latest.get('ema200')

            if ema20 and ema50:
                if ema200:
                    if ema20 > ema50 > ema200: trend = "Strong Bullish"
                    elif ema20 < ema50 < ema200: trend = "Strong Bearish"
                    elif ema20 > ema50: trend = "Bullish"
                    else: trend = "Bearish"
                else:
                    trend = "Bullish (ST)" if ema20 > ema50 else "Bearish (ST)"

            bb_pos = "Inside"
            if not pd.isna(latest.get('BBU_20_2.0')) and latest['close'] > latest['BBU_20_2.0']:
                bb_pos = "Overbought"
            elif not pd.isna(latest.get('BBL_20_2.0')) and latest['close'] < latest['BBL_20_2.0']:
                bb_pos = "Oversold"

            return {
                "price": round(float(latest['close']), 4),
                "rsi": round(float(latest['rsi']), 2) if not pd.isna(latest.get('rsi')) else "N/A",
                "macd": round(float(latest['MACD_12_26_9']), 6) if not pd.isna(latest.get('MACD_12_26_9')) else "N/A",
                "atr": round(float(latest['atr']), 6) if not pd.isna(latest.get('atr')) else "N/A",
                "adx": round(float(latest['ADX_14']), 2) if not pd.isna(latest.get('ADX_14')) else "N/A",
                "ema20": round(float(ema20), 4) if ema20 else "N/A",
                "ema50": round(float(ema50), 4) if ema50 else "N/A",
                "ema200": round(float(ema200), 4) if ema200 else "N/A",
                "volume_ratio": round(float(latest['v_ratio']), 2) if not pd.isna(latest.get('v_ratio')) else "N/A",
                "bb_status": bb_pos,
                "pivot": round(p, 4),
                "r1": round(r1, 4),
                "s1": round(s1, 4),
                "r2": round(r2, 4),
                "s2": round(s2, 4),
                "trend": trend
            }
        except Exception as e:
            logger.error(f"Error: {e}")
            return {"price": round(float(df.iloc[-1]['close']), 4), "trend": "Error"}
