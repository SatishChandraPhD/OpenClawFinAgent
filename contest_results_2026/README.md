## Files

The following files are included as part of the contest submission:

- orders.jsonl  
  Time-ordered trading actions during the evaluation period

- daily_equity.csv  
  Daily portfolio value normalized to an initial capital of $100,000

- final_portfolio.json  
  Final portfolio value at the end of the evaluation period

- metrics.json  
  Performance metrics including cumulative return, Sharpe ratio, maximum drawdown, and volatility

- alpaca_portfolio_snapshot.png  
  Screenshot of Alpaca account showing final portfolio value


## Compliance

The submitted files conform to the requirements of SecureFinAI Contest 2026 Task V:
https://open-finance-lab.github.io/SecureFinAI_Contest_2026/


## Important Note

The Alpaca account contained pre-existing positions due to prior development of the trading system. No new account was created for the contest period.

To ensure fair comparison and compliance with contest requirements, all results have been normalized to an initial capital of $100,000 as of April 20, 2026.

## Reproducibility

Results were generated using:
evaluation/generate_submission_package.py


GitHub path:
https://github.com/SatishChandraPhD/OpenClawFinAgent/tree/main/evaluation


## Presentation

Slides for the conference presentation, explaining the approach and results, are attached.
