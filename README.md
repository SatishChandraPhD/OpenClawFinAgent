# OpenClawFinAgent
Code for SecureFinAI Contest 2026 Task5 as well as revisions to the code along with corresponding Papers


# OpenClaw-FinAgent

LLM-enhanced agentic trading system developed for SecureFinAI 2026 Task V.

## Architecture

Hybrid decision model combining:

• technical indicators  
• LLM sentiment signals  
• macro reasoning signals  
• risk-aware portfolio management  

## Trading setup

Broker: Alpaca paper trading  
Initial capital: 100000 USD  
Assets:

AAPL  
MSFT  
NVDA  
AMZN  
JPM  
JNJ  
PFE  
XOM  
SPY  
GLD  

## Execution

Run continuously:

python run_trading_system.py

## Evaluation window

Apr 20 – May 1 2026

## Metrics

CR — cumulative return  
SR — Sharpe ratio  
MD — max drawdown  
DV — daily volatility  
AV — annualized volatility  

Final metrics generated using:

python evaluation/generate_contest_submission.py

## Reproducibility

All trading decisions logged to:

logs/equity.csv  
logs/orders.jsonl  

Repository contains stable version used during contest evaluation.
Note: The repository contains the stable implementation used for live paper trading during the SecureFinAI Task V evaluation period (Apr 20 – May 1, 2026). 
Experimental prototypes and backtesting utilities are excluded to ensure reproducibility.

run_trading_system.py:
Supervisory script that runs the trading loop continuously and automatically restarts execution in case of network interruptions or temporary failures. This ensures uninterrupted operation during the contest evaluation period.

