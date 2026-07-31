import os
import time
import requests
import pandas as pd
from telegram import Bot

TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

bot = Bot(token=TOKEN)

EMA_PERIOD = 50
last_signal = None


def get_xauusd_data():
    # Temporary test feed (we will connect a better XAUUSD feed next)
    url = "https://api.metals.live/v1/spot/gold"
    r = requests.get(url, timeout=10)
    data = r.json()

    price = float(data[0]["price"])
    return price


def send_alert(message):
    bot.send_message(
        chat_id=CHAT_ID,
        text=message
    )


def main():
    global last_signal

    while True:
        try:
            price = get_xauusd_data()

            # EMA logic will be added after connecting candle data
            print("XAUUSD price:", price)

            time.sleep(60)

        except Exception as e:
            print(e)
            time.sleep(60)


if __name__ == "__main__":
    main()
