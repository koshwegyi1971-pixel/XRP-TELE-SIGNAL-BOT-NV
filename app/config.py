import os
from dotenv import load_dotenv

load_dotenv()

# Telegram Config
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# AI Config
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini")

# Market Config
SYMBOL = os.getenv("SYMBOL", "XRP/USDT")
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", "3600"))
TIMEFRAMES = ["15m", "1h", "4h"]

# Exchange Config
EXCHANGE_ID = os.getenv("EXCHANGE_ID", "kraken")

# Health Check Port
PORT = int(os.getenv("PORT", "10000"))
