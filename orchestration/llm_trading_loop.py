"""
LLM-enhanced trading loop

combines:

technical indicators
LLM stock sentiment
macro sentiment
risk management
execution
logging

supports:

live trading
simulation mode (outside market hours)
"""

import time
from datetime import datetime
import pytz

from data.alpaca_data_loader import AlpacaDataLoader

from signals.indicators import IndicatorEngine

from signals.technical_signal_engine import TechnicalSignalEngine

from llm.llm_signal_engine import LLMSignalEngine

from llm.macro_signal_engine import MacroSignalEngine

from risk.risk_manager import RiskManager

from execution.alpaca_executor import AlpacaExecutor

from portfolio.equity_tracker import EquityTracker

from config.settings import (

    ASSET_UNIVERSE,

    INDICATOR_CONFIG,

    SIGNAL_CONFIG,

    TRADING_CONFIG,

    RISK_CONFIG,

    LOGGING_CONFIG,

    LLM_CONFIG

)

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

def combine_signals(

    technical_signal,

    llm_signal,

    macro_signal

):

    tech_score = technical_signal["score"]

    stock_score = llm_signal["sentiment_score"]

    macro_score = macro_signal["macro_score"]

    combined_score = (

        SIGNAL_CONFIG["TECHNICAL_WEIGHT"]

        * tech_score

        +

        SIGNAL_CONFIG["LLM_WEIGHT"]

        * stock_score

        +

        SIGNAL_CONFIG["MACRO_WEIGHT"]

        * macro_score

    )

    if combined_score >= SIGNAL_CONFIG["BUY_THRESHOLD"]:

        action = "BUY"

    elif combined_score <= SIGNAL_CONFIG["SELL_THRESHOLD"]:

        action = "SELL"

    else:

        action = "HOLD"

    confidence = round(

        min(abs(combined_score) / 2, 1),

        2

    )

    rationale = technical_signal["rationale"]

    return {

        "action": action,

        "score": combined_score,

        "confidence": confidence,

        "rationale": rationale

    }


# ============================

def run_llm_trading_loop():

    print("\nStarting LLM-enhanced trading loop\n")

    loader = AlpacaDataLoader()

    indicator_engine = IndicatorEngine(

        INDICATOR_CONFIG

    )

    combined_signal_config = {

        **SIGNAL_CONFIG,

        **INDICATOR_CONFIG

    }

    signal_engine = TechnicalSignalEngine(

        combined_signal_config

    )

    llm_engine = LLMSignalEngine(

        LLM_CONFIG

    )

    macro_engine = MacroSignalEngine(

        LLM_CONFIG

    )

    risk_manager = RiskManager(

        TRADING_CONFIG,

        RISK_CONFIG,

        SIGNAL_CONFIG

    )

    executor = AlpacaExecutor()

    equity_tracker = EquityTracker(

        executor,

        LOGGING_CONFIG

    )

    risk_manager.sync_positions_from_broker(

        executor

    )

    interval_minutes = TRADING_CONFIG["INTERVAL_MINUTES"]

    while True:

        print("\n==============================")

        print(

            "Cycle time (UTC):",

            datetime.utcnow()

        )

        market_open_flag = market_is_open()

        print(

            "US market open:",

            market_open_flag

        )

        account_info = executor.get_account_info()

        portfolio_value = account_info["equity"]

        cash_available = account_info["cash"]

        print(

            "Portfolio value:",

            portfolio_value

        )

        macro_signal = macro_engine.generate_signal()

        print(

            "Macro sentiment:",

            macro_signal["macro_score"]

        )

        for symbol in ASSET_UNIVERSE:

            print(f"\nProcessing: {symbol}")

            try:

                df = loader.get_recent_bars(symbol)

                if df is None:

                    continue

                df_ind = indicator_engine.compute_indicators(df)

                technical_signal = signal_engine.generate_signal(

                    df_ind

                )

                llm_signal = llm_engine.generate_signal(symbol)

                combined_signal = combine_signals(

                    technical_signal,

                    llm_signal,

                    macro_signal

                )

                price = float(

                    df_ind.iloc[-1]["Close"]

                )

                atr = float(

                    df_ind.iloc[-1]["atr"]

                )

                decision = risk_manager.evaluate_trade(

                    symbol,

                    combined_signal,

                    price,

                    atr,

                    portfolio_value,

                    cash_available

                )

                if market_open_flag:

                    executor.execute_trade(

                        decision,

                        price

                    )

                else:

                    print(

                        f"SIMULATION MODE: {decision['action']} {symbol} @ {price}"

                    )

            except Exception as e:

                print(f"Error: {symbol}", e)

        equity_tracker.log_equity()

        print(f"\nSleeping {interval_minutes} minutes")

        time.sleep(

            interval_minutes * 60

        )


# ============================

if __name__ == "__main__":

    run_llm_trading_loop()