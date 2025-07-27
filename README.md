# Wallet Risk Scoring – Round 2 Assignment

## 1. Data Collection
We used the Moralis API to fetch the on-chain ERC20 transaction history for 100 Ethereum wallet addresses.
- Endpoint: `/wallet_address/erc20/transfers?chain=eth`
- For each wallet, we retrieved:
  - Token transfers (sent and received)
  - Token values and timestamps

## 2. Feature Engineering
To quantify wallet activity and derive a risk score, we engineered the following features:
- **total_value**: Sum of all transaction amounts (normalized to token decimals).
  - Indicates how much volume the wallet is transacting.
- **txn_count**: Total number of token transfers.
  - Reflects wallet activeness and frequency.
- **unique_tokens**: Number of distinct tokens interacted with.
  - Helps assess diversification or exposure risk.

### Justification:
These features were chosen as they provide a holistic view of wallet behavior in terms of volume, frequency, and diversity — all relevant indicators for potential lending/borrowing risk.

## 3. Risk Scoring Methodology
We followed a normalized, weighted scoring method:
- Each feature was normalized using Min-Max scaling.
- Weighted score calculation:
score = 0.5 * total_value_norm + 0.3 * txn_count_norm + 0.2 * unique_tokens_norm

- The final score is scaled to a 0–1000 range (rounded integer).

### Why These Weights?
- **total_value** has the highest influence as it reflects transaction capacity.
- **txn_count** suggests operational frequency, useful for evaluating engagement.
- **unique_tokens** gives context on how diverse the activity is, helpful in identifying risky or stable behaviors.

## 4. Output
We produced a CSV file with the following structure:

| wallet_id                                   | score |
|--------------------------------------------|-------|
| 0xfaa0768bde629806739c3a4620656c5d26f44ef2 | 732   |
| ...                                        | ...   |

## 5. Tools Used
- Python (Pandas, NumPy, Requests)
- Moralis API
- CSV for output

---

## Notes
- The model is easily extensible to include protocol-level data (e.g., borrow/supply metrics from Compound).
- Can be improved by incorporating lending-specific indicators like liquidation history, collateralization ratios, etc.

