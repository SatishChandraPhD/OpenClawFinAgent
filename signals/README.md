signals/

This folder contains technical signal generation logic.

technical_signal_engine.py:
Implements rule-based trading signals derived from technical indicators such as trend, momentum, and volatility measures.

indicators.py:
Computes underlying technical indicators (e.g. EMA, RSI, MACD, ATR) used by the technical signal engine.

These modules provide deterministic market signals which act as the primary driver of trading decisions.
