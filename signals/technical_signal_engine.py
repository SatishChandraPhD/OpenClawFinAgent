"""
Technical Signal Engine
Converts indicators into trading signals
"""


class TechnicalSignalEngine:

    def __init__(self, config):

        self.config = config


    def generate_signal(self, df):

        latest = df.iloc[-1]

        ema_short = float(latest["ema_short"])
        ema_long = float(latest["ema_long"])

        rsi = float(latest["rsi"])

        macd = float(latest["macd"])
        macd_signal = float(latest["macd_signal"])

        score = 0
        reasons = []

        # ======================
        # TREND SIGNAL
        # ======================

        if ema_short > ema_long:

            score += 1
            reasons.append("Uptrend")

        elif ema_short < ema_long:

            score -= 1
            reasons.append("Downtrend")

        # ======================
        # MOMENTUM SIGNAL
        # ======================

        if macd > macd_signal:

            score += 1
            reasons.append("Bullish momentum")

        elif macd < macd_signal:

            score -= 1
            reasons.append("Bearish momentum")

        # ======================
        # RSI FILTER
        # ======================

        if rsi > self.config["RSI_OVERBOUGHT"]:

            score -= 1
            reasons.append("Overbought")

        elif rsi < self.config["RSI_OVERSOLD"]:

            score += 1
            reasons.append("Oversold")

        # ======================
        # FINAL DECISION
        # ======================

        if score >= self.config["BUY_THRESHOLD"]:

            action = "BUY"

        elif score <= self.config["SELL_THRESHOLD"]:

            action = "SELL"

        else:

            action = "HOLD"

        confidence = round(abs(score) / 3, 2)

        rationale = ", ".join(reasons)

        return {

            "action": action,

            "score": int(score),

            "confidence": float(confidence),

            "rationale": rationale
        }