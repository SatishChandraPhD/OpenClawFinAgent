"""
Baseline Trading Agent

Implements deterministic technical trading logic
used as control model for evaluating LLM-enhanced agent.

Strategy components:
EMA crossover
RSI filter
MACD momentum
ATR stop loss
risk-based position sizing
"""



"""
Main Trading Loop

Phase-1 baseline trading engine
with portfolio sync + equity logging
"""



import time
from datetime import datetime
import pytz

from data.alpaca_data_loader import AlpacaDataLoader
from signals.indicators import IndicatorEngine
from signals.technical_signal_engine import TechnicalSignalEngine
from risk.risk_manager import RiskManager
from execution.alpaca_executor import AlpacaExecutor
from portfolio.equity_tracker import EquityTracker

from config.settings import (
    ASSET_UNIVERSE,
    INDICATOR_CONFIG,
    SIGNAL_CONFIG,
    TRADING_CONFIG,
    RISK_CONFIG,
    LOGGING_CONFIG
)


# ============================
# MARKET HOURS CHECK
# ============================

def market_is_open():

    eastern = pytz.timezone("US/Eastern")

    now = datetime.now(eastern)

    if now.weekday() >= 5:
        return False

    market_open = now.replace(
        hour=9,
        minute=30,
        second=0,
        microsecond=0
    )

    market_close = now.replace(
        hour=16,
        minute=0,
        second=0,
        microsecond=0
    )

    return market_open <= now <= market_close


# ============================
# MAIN LOOP
# ============================

def run_trading_loop():

    print("\nStarting trading loop...\n")

    loader = AlpacaDataLoader()

    indicator_engine = IndicatorEngine(INDICATOR_CONFIG)

    combined_signal_config = {
        **SIGNAL_CONFIG,
        **INDICATOR_CONFIG
    }

    signal_engine = TechnicalSignalEngine(combined_signal_config)

    risk_manager = RiskManager(
        TRADING_CONFIG,
        RISK_CONFIG
    )

    executor = AlpacaExecutor()

    # sync existing Alpaca positions
    risk_manager.sync_positions_from_broker(executor)

    equity_tracker = EquityTracker(
        executor,
        LOGGING_CONFIG
    )

    interval_minutes = TRADING_CONFIG["INTERVAL_MINUTES"]

    while True:

        if not market_is_open():

            print("Market closed... waiting")

            time.sleep(300)

            continue


        print("\nRunning trading cycle:", datetime.utcnow())

        account_info = executor.get_account_info()

        portfolio_value = account_info["equity"]

        cash_available = account_info["cash"]


        for symbol in ASSET_UNIVERSE:

            print(f"\nProcessing {symbol}")

            try:

                df = loader.get_recent_bars(symbol)

                if df is None:
                    continue


                df_ind = indicator_engine.compute_indicators(df)


                signal = signal_engine.generate_signal(df_ind)


                latest_price = float(df_ind.iloc[-1]["Close"])

                atr = float(df_ind.iloc[-1]["atr"])


                decision = risk_manager.evaluate_trade(

                    symbol,
                    signal,
                    latest_price,
                    atr,
                    portfolio_value,
                    cash_available

                )


                executor.execute_trade(

                    decision,
                    latest_price

                )


            except Exception as e:

                print(f"Error processing {symbol}: {e}")


        equity_tracker.log_equity()


        print(f"\nSleeping {interval_minutes} minutes...\n")

        time.sleep(interval_minutes * 60)


# ============================

if __name__ == "__main__":

    run_trading_loop()