orchestration/

This folder contains the main trading loop implementations.

llm_trading_loop.py:
Stable version of the live trading engine used during the SecureFinAI Task 5 evaluation period (Apr 20 – May 1). The loop integrates technical indicators, LLM-based sentiment signals, macro signals, and risk management to generate portfolio actions.

baseline_trading_loop.py:
Reference implementation that executes trading decisions using only deterministic technical indicators. This file is provided for comparison purposes and is not used during the contest evaluation window.
