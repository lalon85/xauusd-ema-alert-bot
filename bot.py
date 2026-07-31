import time
import requests

from config import (
    TELEGRAM_TOKEN,
    TELEGRAM_CHAT_ID,
    CHECK_INTERVAL
)

from data import get_candles
from strategy import check_signal


last_alert = None


def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }

    requests.post(url, json=payload, timeout=10)


def main():

    global last_alert

    print("XAUUSD EMA50 Telegram Bot Started")

    while True:

        try:
            candles = get_candles()

            signal = check_signal(candles)

            if signal:

                alert_key = (
                    signal["signal"],
                    signal["time"]
                )

                # Prevent duplicate alerts
                if alert_key != last_alert:

                    message = (
                        f"XAUUSD M1 {signal['signal']}\n\n"
                        f"Price: {signal['price']}\n"
                        f"EMA50: {signal['ema']}\n"
                        f"Candle: {signal['time']}"
                    )

                    send_telegram(message)

                    last_alert = alert_key

                    print(message)

        except Exception as e:
            print("Error:", e)

        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()
