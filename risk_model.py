# risk_model.py

import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

# Load transaction data
df = pd.read_csv("data/compound_transactions.csv")

# --- Feature Engineering ---
grouped = df.groupby("wallet_id").agg({
    "value": ["sum", "count"],
    "token_symbol": pd.Series.nunique
})

# Rename columns
grouped.columns = ["total_value", "txn_count", "unique_tokens"]
grouped.reset_index(inplace=True)

# --- Log Transformation to reduce skewness ---
grouped["total_value"] = np.log1p(grouped["total_value"])
grouped["txn_count"] = np.log1p(grouped["txn_count"])

# --- Normalization using MinMaxScaler ---
scaler = MinMaxScaler()
grouped[["total_value_norm", "txn_count_norm", "unique_tokens_norm"]] = scaler.fit_transform(
    grouped[["total_value", "txn_count", "unique_tokens"]]
)

# --- Weighted Score Calculation ---
grouped["score"] = (
    0.5 * grouped["total_value_norm"] +
    0.3 * grouped["txn_count_norm"] +
    0.2 * grouped["unique_tokens_norm"]
)

# Scale to 0–1000
grouped["score"] = (grouped["score"] * 1000).round().astype(int)

# --- Export Result ---
grouped[["wallet_id", "score"]].to_csv("risk_scores.csv", index=False)
print("✅ Risk scores written to risk_scores.csv")
