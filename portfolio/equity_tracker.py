"""
Equity Tracker

Logs portfolio value for contest evaluation
"""

import csv
import os
from datetime import datetime


class EquityTracker:

    def __init__(self, executor, config):

        self.executor = executor

        self.file = config["EQUITY_FILE"]


    def log_equity(self):

        account = self.executor.get_account_info()

        equity = account["equity"]

        cash = account["cash"]

        buying_power = account["buying_power"]

        file_exists = os.path.exists(self.file)

        with open(self.file, "a", newline="") as f:

            writer = csv.writer(f)

            if not file_exists:

                writer.writerow(

                    [

                        "timestamp",

                        "equity",

                        "cash",

                        "buying_power"

                    ]

                )

            writer.writerow(

                [

                    datetime.utcnow().isoformat(),

                    equity,

                    cash,

                    buying_power

                ]

            )

        print(f"Equity logged: {equity}")