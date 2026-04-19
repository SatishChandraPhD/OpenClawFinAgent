"""
Supervisor for OpenClaw-FinAgent trading loop

Automatically restarts trading loop if crash occurs.
Ensures robustness during live trading sessions.
"""

import time
import traceback

import orchestration.llm_trading_loop as trading_loop


RESTART_DELAY_SECONDS = 60


def start_trading():

    while True:

        try:

            print("\n==============================")
            print("Starting LLM trading loop")
            print("==============================\n")

            trading_loop.run_llm_trading_loop()

        except Exception as e:

            print("\n==============================")
            print("Trading loop crashed")
            print("==============================\n")

            print(str(e))

            traceback.print_exc()

            print(f"\nRestarting in {RESTART_DELAY_SECONDS} seconds...\n")

            time.sleep(RESTART_DELAY_SECONDS)


if __name__ == "__main__":

    print("\n==============================")
    print("Starting OpenClaw-FinAgent Supervisor")
    print("==============================\n")

    start_trading()