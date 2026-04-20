"""
Technical Indicators Module
"""

import pandas as pd

from ta.trend import EMAIndicator
from ta.trend import MACD

from ta.momentum import RSIIndicator

from ta.volatility import AverageTrueRange


class IndicatorEngine:

    def __init__(self, config):

        self.config = config


    def compute_indicators(self, df):

        df = df.copy()

        # =========================
        # EMA
        # =========================

        ema_short = EMAIndicator(
            close=df["Close"],
            window=self.config["EMA_SHORT_WINDOW"]
        )

        ema_long = EMAIndicator(
            close=df["Close"],
            window=self.config["EMA_LONG_WINDOW"]
        )

        df["ema_short"] = ema_short.ema_indicator()

        df["ema_long"] = ema_long.ema_indicator()

        # =========================
        # RSI
        # =========================

        rsi = RSIIndicator(
            close=df["Close"],
            window=self.config["RSI_WINDOW"]
        )

        df["rsi"] = rsi.rsi()

        # =========================
        # MACD
        # =========================

        macd = MACD(
            close=df["Close"],
            window_fast=self.config["MACD_FAST"],
            window_slow=self.config["MACD_SLOW"],
            window_sign=self.config["MACD_SIGNAL"]
        )

        df["macd"] = macd.macd()

        df["macd_signal"] = macd.macd_signal()

        # =========================
        # ATR
        # =========================

        atr = AverageTrueRange(
            high=df["High"],
            low=df["Low"],
            close=df["Close"],
            window=self.config["ATR_WINDOW"]
        )

        df["atr"] = atr.average_true_range()

        return df