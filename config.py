import os

# API keys from environment variables
TWELVE_API_KEY = os.getenv("TWELVE_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Market settings
SYMBOL = "XAU/USD"
INTERVAL = "1min"

# Strategy
EMA_PERIOD = 50

# Check every minute
CHECK_INTERVAL = 60
