import json
import os
from datetime import datetime

BALANCE_FILE = "sim_balance.json"
DEFAULT_BALANCE = 1000.00  # RM1000 default modal

def load_balance():
    if not os.path.exists(BALANCE_FILE):
        return {"balance": DEFAULT_BALANCE, "last_updated": str(datetime.utcnow())}
    
    try:
        with open(BALANCE_FILE, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"[WARNING] Failed to load balance: {e}")
        return {"balance": DEFAULT_BALANCE, "last_updated": str(datetime.utcnow())}

def save_balance(new_balance: float):
    data = {
        "balance": new_balance,
        "last_updated": str(datetime.utcnow())
    }
    try:
        with open(BALANCE_FILE, "w") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f"[ERROR] Failed to save balance: {e}")

def simulate_trade_and_update_balance(profit_loss: float):
    """
    Simulate a trade outcome. `profit_loss` is in RM. Can be +ve or -ve.
    """
    data = load_balance()
    new_balance = round(data["balance"] + profit_loss, 2)
    save_balance(new_balance)
    return new_balance
