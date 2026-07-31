import requests
import pandas as pd
from config import TWELVE_API_KEY, SYMBOL, INTERVAL


def get_candles():
    url = "https://api.twelvedata.com/time_series"

    params = {
        "symbol": SYMBOL,
        "interval": INTERVAL,
        "outputsize": 100,
        "apikey": TWELVE_API_KEY
    }

    response = requests.get(url, params=params, timeout=10)
    data = response.json()

    if "values" not in data:
        print("Twelve Data error:", data)
        return None

    df = pd.DataFrame(data["values"])

    df["close"] = df["close"].astype(float)
    df["datetime"] = pd.to_datetime(df["datetime"])

    # Oldest candle first
    df = df.sort_values("datetime")

    return df


def get_latest_closed_candle():
    df = get_candles()

    if df is None:
        return None

    # Remove the newest candle because it may still be forming
    closed = df.iloc[-2]

    return closed
