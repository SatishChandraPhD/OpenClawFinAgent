"""
Risk Manager

Position sizing
Stop-loss handling
Portfolio constraints
Broker sync support
"""

import math


class RiskManager:

    def __init__(
        self,
        trading_config,
        risk_config,
        signal_config
    ):

        self.trading_config = trading_config
        self.risk_config = risk_config
        self.signal_config = signal_config

        # internal state
        self.positions = {}
        self.entry_prices = {}
        self.stop_prices = {}

    # ============================
    # Broker sync
    # ============================

    def sync_positions_from_broker(self, executor):

        alpaca_positions = executor.api.list_positions()

        for pos in alpaca_positions:

            symbol = pos.symbol

            qty = int(float(pos.qty))

            avg_price = float(pos.avg_entry_price)

            self.positions[symbol] = qty

            self.entry_prices[symbol] = avg_price

            self.stop_prices[symbol] = avg_price * 0.95

        print("\nBroker positions synced:")

        print(self.positions)

    # ============================
    # position sizing
    # ============================

    def calculate_position_size(
        self,
        price,
        portfolio_value,
        cash_available
    ):

        max_position_value = (
            portfolio_value
            * self.trading_config["MAX_POSITION_PCT"]
        )

        shares = math.floor(
            min(max_position_value, cash_available) / price
        )

        return max(shares, 0)

    # ============================
    # stop loss calculation
    # ============================

    def compute_stop_loss(
        self,
        price,
        atr
    ):

        return price - (
            atr * self.risk_config["ATR_STOP_MULTIPLIER"]
        )

    # ============================
    # main decision logic
    # ============================

    def evaluate_trade(

        self,

        symbol,

        signal,

        price,

        atr,

        portfolio_value,

        cash_available

    ):

        action = signal["action"]

        score = signal["score"]

        confidence = signal["confidence"]

        rationale = signal["rationale"]

        buy_threshold = self.signal_config.get(
            "BUY_THRESHOLD",
            1.0
        )

        sell_threshold = self.signal_config.get(
            "SELL_THRESHOLD",
            -1.0
        )

        # ======================
        # SELL logic
        # ======================

        if symbol in self.positions:

            entry_price = self.entry_prices[symbol]

            stop_price = self.stop_prices[symbol]

            # ATR stop-loss
            if price <= stop_price:

                shares = self.positions[symbol]

                print(f"Stop triggered for {symbol}")

                return {

                    "symbol": symbol,

                    "action": "SELL",

                    "shares": shares,

                    "stop_loss": None,

                    "confidence": confidence,

                    "rationale": "ATR stop loss triggered"

                }

            # signal based sell
            if score <= sell_threshold:

                shares = self.positions[symbol]

                return {

                    "symbol": symbol,

                    "action": "SELL",

                    "shares": shares,

                    "stop_loss": None,

                    "confidence": confidence,

                    "rationale": rationale

                }

            # already holding
            return {

                "symbol": symbol,

                "action": "HOLD",

                "shares": 0,

                "stop_loss": stop_price,

                "confidence": confidence,

                "rationale": rationale

            }

        # ======================
        # BUY logic
        # ======================

        if score >= buy_threshold:

            shares = self.calculate_position_size(

                price,

                portfolio_value,

                cash_available

            )

            if shares > 0:

                stop_price = self.compute_stop_loss(

                    price,

                    atr

                )

                self.positions[symbol] = shares

                self.entry_prices[symbol] = price

                self.stop_prices[symbol] = stop_price

                return {

                    "symbol": symbol,

                    "action": "BUY",

                    "shares": shares,

                    "stop_loss": stop_price,

                    "confidence": confidence,

                    "rationale": rationale

                }

        # ======================
        # HOLD logic
        # ======================

        return {

            "symbol": symbol,

            "action": "HOLD",

            "shares": 0,

            "stop_loss": None,

            "confidence": confidence,

            "rationale": rationale

        }