import os
import requests
import pandas as pd
from tqdm import tqdm

MORALIS_API_KEY = os.getenv("MORALIS_API_KEY")  # Set this in your environment
MORALIS_API_URL = "https://deep-index.moralis.io/api/v2.2"
CHAIN = "eth"

df = pd.read_csv("data/wallets.csv")

all_data = []

headers = {
    "accept": "application/json",
    "X-API-Key": MORALIS_API_KEY
}

for wallet in tqdm(df["wallet_id"], desc="Fetching data"):
    url = f"{MORALIS_API_URL}/{wallet}/erc20/transfers?chain={CHAIN}"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        txns = response.json().get("result", [])
        for txn in txns:
            all_data.append({
                "wallet_id": wallet,
                "block_number": txn.get("block_number"),
                "token_symbol": txn.get("token_symbol"),
                "value": float(txn.get("value", 0)) / (10 ** int(txn.get("token_decimals", 0))),
                "to_address": txn.get("to_address"),
                "from_address": txn.get("from_address")
            })
    except Exception as e:
        print(f"Error for {wallet}: {e}")

df_out = pd.DataFrame(all_data)
df_out.to_csv("data/compound_transactions.csv", index=False)
print("✅ All transactions saved to data/compound_transactions.csv")
