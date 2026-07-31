import os
import time
import requests
import pandas as pd
from telegram import Bot

TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

bot = Bot(token=TOKEN)

last_signal = None


def get_candles():
    # Placeholder connection - we will connect the final XAUUSD feed next
    url = "https://api.metals.live/v1/spot/gold"

    r = requests.get(url, timeout=10)
    data = r.json()

    price = float(data[0]["price"])

    return price


def calculate_ema(prices):
    series = pd.Series(prices)
    return series.ewm(span=50).mean().iloc[-1]


def send_alert(text):
    bot.send_message(
        chat_id=CHAT_ID,
        text=text
    )


def main():
    global last_signal

    prices = []

    while True:
        try:
            price = get_candles()
            prices.append(price)

            if len(prices) >= 50:

                ema50 = calculate_ema(prices)

                if price > ema50 and last_signal != "BUY":
                    send_alert(
                        f"🟢 XAUUSD\n\n"
                        f"CLOSED ABOVE EMA 50\n"
                        f"Price: {price}\n"
                        f"EMA50: {ema50}"
                    )
                    last_signal = "BUY"


                elif price < ema50 and last_signal != "SELL":
                    send_alert(
                        f"🔴 XAUUSD\n\n"
                        f"CLOSED BELOW EMA 50\n"
                        f"Price: {price}\n"
                        f"EMA50: {ema50}"
                    )
                    last_signal = "SELL"


            time.sleep(60)

        except Exception as e:
            print(e)
            time.sleep(60)


if __name__ == "__main__":
    main()
