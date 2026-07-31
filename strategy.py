import pandas as pd
from config import EMA_PERIOD


def check_signal(df):

    if df is None or len(df) < EMA_PERIOD:
        return None

    # Calculate EMA 50
    df["ema50"] = df["close"].ewm(
        span=EMA_PERIOD,
        adjust=False
    ).mean()

    last = df.iloc[-1]

    close_price = last["close"]
    ema_value = last["ema50"]

    # Price above EMA = bullish confirmation
    if close_price > ema_value:
        return {
            "signal": "BUY",
            "price": close_price,
            "ema": ema_value,
            "time": last["datetime"]
        }

    # Price below EMA = bearish confirmation
    if close_price < ema_value:
        return {
            "signal": "SELL",
            "price": close_price,
            "ema": ema_value,
            "time": last["datetime"]
        }

    return None
