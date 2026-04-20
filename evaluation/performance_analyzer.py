"""
Performance Analyzer

Computes trading metrics from equity log
Compatible with both header and no-header equity.csv
"""

import pandas as pd
import numpy as np


def load_equity_curve(file_path):

    df = pd.read_csv(file_path)

    # case 1 — file has headers
    if "equity" in df.columns:

        return df

    # case 2 — file has no headers
    elif df.shape[1] == 4:

        df.columns = [
            "timestamp",
            "equity",
            "cash",
            "buying_power"
        ]

        return df

    else:

        raise ValueError("Unexpected equity.csv format")


def analyze_performance(equity_file="logs/equity.csv"):

    df = load_equity_curve(equity_file)

    df["returns"] = df["equity"].pct_change()

    df = df.dropna()

    cumulative_return = (

        df["equity"].iloc[-1] /
        df["equity"].iloc[0] - 1

    )

    sharpe_ratio = (

        np.sqrt(252)
        * df["returns"].mean()
        / df["returns"].std()
    ) if df["returns"].std() != 0 else 0

    running_max = df["equity"].cummax()

    drawdown = (

        df["equity"] - running_max
    ) / running_max

    max_drawdown = drawdown.min()

    volatility = df["returns"].std()

    results = {

        "cumulative_return": cumulative_return,

        "sharpe_ratio": sharpe_ratio,

        "max_drawdown": max_drawdown,

        "volatility": volatility,

        "observations": len(df)

    }

    return results


if __name__ == "__main__":

    results = analyze_performance()

    print("\nPerformance Summary\n")

    for k, v in results.items():

        print(f"{k}: {round(v,4)}")