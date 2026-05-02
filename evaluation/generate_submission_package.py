import pandas as pd
import json
import os
import shutil

# =========================
# PATH SETUP
# =========================
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

#INPUT_EQUITY = os.path.join(BASE_DIR, "logs", "contest", "equity_contest.csv")

INPUT_EQUITY = os.path.join(
    BASE_DIR,
    "logs",
    "contest_submission",
    "2026-05-02",
    "equity_contest.csv"
)

INPUT_ORDERS = os.path.join(
    BASE_DIR,
    "logs",
    "contest_submission",
    "2026-05-02",
    "orders_contest.jsonl"
)

OUTPUT_DIR = os.path.join(BASE_DIR, "logs", "final_submission")

os.makedirs(OUTPUT_DIR, exist_ok=True)

# =========================
# 1. LOAD EQUITY
# =========================
df = pd.read_csv(INPUT_EQUITY)

# Normalize column names if needed
if "timestamp" not in df.columns:
    if len(df.columns) >= 2:
        df.columns = ["timestamp", "equity"] + list(df.columns[2:])
    else:
        raise ValueError("Equity file format unexpected")

df["timestamp"] = pd.to_datetime(df["timestamp"])

# Ensure correct order
df = df.sort_values("timestamp")

df["date"] = df["timestamp"].dt.date

# =========================
# 2. DAILY EQUITY (LAST VALUE PER DAY)
# =========================
daily = df.groupby("date").tail(1)[["date", "equity"]].copy()

daily["date"] = daily["date"].astype(str)

# =========================
# 3. NORMALIZATION (CRITICAL)
# =========================
initial_equity = daily["equity"].iloc[0]

if initial_equity == 0:
    raise ValueError("Initial equity is zero, cannot normalize")

scale = 100000 / initial_equity

daily["equity"] = daily["equity"] * scale

# =========================
# 4. SAVE DAILY EQUITY
# =========================
daily.to_csv(os.path.join(OUTPUT_DIR, "daily_equity.csv"), index=False)

# =========================
# 5. FINAL SNAPSHOT (NORMALIZED)
# =========================
final_equity = float(daily["equity"].iloc[-1])

snapshot = {
    "timestamp": str(daily["date"].iloc[-1]),
    "portfolio_value": final_equity
}

with open(os.path.join(OUTPUT_DIR, "final_portfolio.json"), "w") as f:
    json.dump(snapshot, f, indent=4)

# =========================
# 6. COPY ORDERS
# =========================
if not os.path.exists(INPUT_ORDERS):
    raise FileNotFoundError(f"Orders file not found: {INPUT_ORDERS}")

shutil.copy(INPUT_ORDERS, os.path.join(OUTPUT_DIR, "orders.jsonl"))

# =========================
# 7. METRICS (FROM NORMALIZED DATA)
# =========================
returns = daily["equity"].pct_change().dropna()

metrics = {
    "cumulative_return": float(daily["equity"].iloc[-1] / daily["equity"].iloc[0] - 1),
    "daily_volatility": float(returns.std()),
    "annualized_volatility": float(returns.std() * (252 ** 0.5)),
    "sharpe_ratio": float((returns.mean() / returns.std()) * (252 ** 0.5)) if returns.std() != 0 else 0,
    "max_drawdown": float((daily["equity"] / daily["equity"].cummax() - 1).min())
}

with open(os.path.join(OUTPUT_DIR, "metrics.json"), "w") as f:
    json.dump(metrics, f, indent=4)

# =========================
# DONE
# =========================
print("✅ Submission package created successfully!")
print("📁 Location:", OUTPUT_DIR)
print("📊 Initial equity normalized to:", daily["equity"].iloc[0])
print("📊 Final equity:", final_equity)