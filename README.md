# XRP TELE SIGNAL BOT NV

A production-grade cryptocurrency trading signal bot for XRP, featuring advanced technical, fundamental, and sentiment analysis, powered by AI via OpenRouter.

## 🚀 Features

- **Advanced TA:** Multi-timeframe technical analysis (15m, 1h, 4h) using professional-grade indicators (EMA, RSI, MACD, ATR, ADX) via `pandas_ta`.
- **Market Regime Detection:** Automatically identifies market conditions (Trending Bull/Bear, Sideways, Volatile) to tailor recommendations.
- **Fundamental & Sentiment Analysis:** Integrates CoinGecko data for XRP fundamentals and the Fear & Greed Index for market sentiment.
- **AI-Powered Insights:** Uses OpenRouter (GPT-4o-mini/GPT-4o) to synthesize all data points into concise, actionable market reports and DCA recommendations.
- **DCA Alerts:** Specific buy/sell zone identification for effective Dollar-Cost Averaging.
- **Telegram Integration:** Automated hourly reports and critical alerts delivered directly to your Telegram.
- **Render Ready:** Optimized for deployment on Render using Docker for high reliability.

## 🛠 Setup & Deployment

### 1. Environment Variables
Create a `.env` file or set the following environment variables in your deployment platform:

- `TELEGRAM_BOT_TOKEN`: Your Telegram Bot API token.
- `TELEGRAM_CHAT_ID`: Your Telegram Chat ID.
- `OPENROUTER_API_KEY`: Your OpenRouter API Key.
- `OPENROUTER_MODEL`: (Optional) The AI model to use (default: `openai/gpt-4o-mini`).
- `SYMBOL`: (Optional) Trading pair (default: `XRP/USDT`).
- `CHECK_INTERVAL`: (Optional) Analysis interval in seconds (default: `3600`).
- `EXCHANGE_ID`: (Optional) CCXT exchange ID (default: `kraken`).

### 2. Deployment on Render
1. Push this repository to your GitHub.
2. Create a new **Web Service** or **Worker** on Render.
3. Connect your GitHub repository.
4. Render will automatically detect the `render.yaml` and `Dockerfile`.
5. Add your environment variables in the Render dashboard.
6. Deploy!

## 📜 Disclaimer
This bot is for informational purposes only. Trading cryptocurrency involves significant risk. Always do your own research (DYOR) before making any investment decisions.
