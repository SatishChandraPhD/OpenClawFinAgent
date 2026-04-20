"""
Alpaca Execution Engine

Places paper trades
Logs orders (orders.jsonl)
Logs signals including HOLD (signals.csv)
Prevents duplicate buys
Prevents invalid sells
"""

import os
import json
import csv

from datetime import datetime

from dotenv import load_dotenv

import alpaca_trade_api as tradeapi


class AlpacaExecutor:

    def __init__(self):

        load_dotenv()

        self.api = tradeapi.REST(

            os.getenv("ALPACA_API_KEY"),

            os.getenv("ALPACA_SECRET_KEY"),

            os.getenv("ALPACA_BASE_URL"),

            api_version="v2"

        )

        # ensure logs directory exists

        os.makedirs("logs", exist_ok=True)


    # =====================================================
    # PLACE ORDER
    # =====================================================

    def place_order(

        self,

        symbol,

        action,

        shares

    ):

        if shares <= 0:

            print(f"Skipping order for {symbol} (shares=0)")

            return None


        side = "buy" if action == "BUY" else "sell"


        print(f"\nPlacing order: {side} {shares} {symbol}")


        order = self.api.submit_order(

            symbol=symbol,

            qty=shares,

            side=side,

            type="market",

            time_in_force="gtc"

        )


        return order


    # =====================================================
    # LOG ORDER
    # =====================================================

    def log_order(

        self,

        decision,

        price

    ):

        log_entry = {

            "timestamp": datetime.utcnow().isoformat(),

            "symbol": decision["symbol"],

            "action": decision["action"],

            "shares": int(decision["shares"]),

            "price": float(price),

            "confidence": float(decision["confidence"]),

            "rationale": str(decision["rationale"])

        }


        file = "logs/orders.jsonl"


        with open(

            file,

            "a",

            encoding="utf-8"

        ) as f:

            f.write(

                json.dumps(log_entry)

                + "\n"

            )


        print("Order logged")


    # =====================================================
    # LOG SIGNAL
    # =====================================================

    def log_signal(

        self,

        decision

    ):

        file = "logs/signals.csv"


        file_exists = os.path.exists(file)


        with open(

            file,

            "a",

            newline="",

            encoding="utf-8"

        ) as f:

            writer = csv.writer(f)


            if not file_exists:

                writer.writerow(

                    [

                        "timestamp",

                        "symbol",

                        "action",

                        "confidence",

                        "rationale"

                    ]

                )


            writer.writerow(

                [

                    datetime.utcnow().isoformat(),

                    decision["symbol"],

                    decision["action"],

                    float(decision["confidence"]),

                    str(decision["rationale"])

                ]

            )


        print("Signal logged")


    # =====================================================
    # GET CURRENT POSITIONS
    # =====================================================

    def get_positions(self):

        positions = self.api.list_positions()


        return {

            p.symbol: float(p.qty)

            for p in positions

        }


    # =====================================================
    # EXECUTE TRADE
    # =====================================================

    def execute_trade(

        self,

        decision,

        latest_price

    ):

        symbol = decision["symbol"]

        action = decision["action"]

        shares = decision["shares"]


        # always log signal once

        self.log_signal(decision)


        positions = self.get_positions()

        current_qty = positions.get(

            symbol,

            0

        )


        # =============================
        # HOLD
        # =============================

        if action == "HOLD":

            print(

                f"HOLD decision for {symbol}"

            )

            return


        # =============================
        # PREVENT DUPLICATE BUY
        # =============================

        if action == "BUY" and current_qty > 0:

            print(

                f"Already holding {symbol}, skipping buy"

            )

            return


        # =============================
        # PREVENT INVALID SELL
        # =============================

        if action == "SELL" and current_qty == 0:

            print(

                f"No position in {symbol}, skipping sell"

            )

            return


        # =============================
        # PLACE ORDER
        # =============================

        order = self.place_order(

            symbol,

            action,

            shares

        )


        if order:

            self.log_order(

                decision,

                latest_price

            )


    # =====================================================
    # ACCOUNT INFO
    # =====================================================

    def get_account_info(self):

        account = self.api.get_account()


        return {

            "equity": float(account.equity),

            "cash": float(account.cash),

            "buying_power": float(account.buying_power)

        }