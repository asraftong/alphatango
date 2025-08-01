import json
import os
from collections import Counter

TOP_SYMBOLS_FILE = "data/top_symbols.json"
OPPORTUNITY_LOG = "data/opportunity_history.json"
TOP_N = 10

def update_top_symbols():
    if not os.path.exists(OPPORTUNITY_LOG):
        return

    try:
        with open(OPPORTUNITY_LOG, "r") as f:
            opportunities = json.load(f)

        symbols = [op["symbol"] for op in opportunities if "symbol" in op]
        counter = Counter(symbols)
        top_symbols = [symbol for symbol, _ in counter.most_common(TOP_N)]

        with open(TOP_SYMBOLS_FILE, "w") as f:
            json.dump(top_symbols, f, indent=2)

    except Exception as e:
        print(f"[TOP SYMBOLS] Gagal update top symbols: {e}")

def get_top_symbols():
    if not os.path.exists(TOP_SYMBOLS_FILE):
        return []

    try:
        with open(TOP_SYMBOLS_FILE, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"[TOP SYMBOLS] Gagal baca top symbols: {e}")
        return []
