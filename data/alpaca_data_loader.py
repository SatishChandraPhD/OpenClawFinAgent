"""
Fetch market data from Alpaca
"""

import os
from dotenv import load_dotenv
import pandas as pd
import alpaca_trade_api as tradeapi
from datetime import datetime, timedelta, timezone


class AlpacaDataLoader:

    def __init__(self):

        load_dotenv()

        self.api = tradeapi.REST(
            os.getenv("ALPACA_API_KEY"),
            os.getenv("ALPACA_SECRET_KEY"),
            os.getenv("ALPACA_BASE_URL"),
            api_version="v2"
        )


    def get_recent_bars(
        self,
        symbol,
        timeframe="15Min",
        lookback_days=5
    ):

        end = datetime.now(timezone.utc)

        start = end - timedelta(days=lookback_days)

        start_str = start.strftime("%Y-%m-%dT%H:%M:%SZ")

        end_str = end.strftime("%Y-%m-%dT%H:%M:%SZ")

        bars = self.api.get_bars(
            symbol,
            timeframe,
            start=start_str,
            end=end_str,
            adjustment='raw',
            feed='iex'   # FREE DATA FEED
        ).df

        if bars.empty:

            print(f"No data for {symbol}")

            return None

        df = bars.reset_index()

        df = df.rename(
            columns={
                "timestamp": "Datetime",
                "open": "Open",
                "high": "High",
                "low": "Low",
                "close": "Close",
                "volume": "Volume"
            }
        )

        return df


    def get_multiple_symbols(self, symbols):

        data = {}

        for symbol in symbols:

            df = self.get_recent_bars(symbol)

            if df is not None:

                data[symbol] = df

        return data