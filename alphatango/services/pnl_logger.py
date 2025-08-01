import csv, os
from datetime import datetime

def log_trade_to_csv(symbol, timestamp, profit_rm, balance_rm):
    d = datetime.now().strftime("%Y-%m-%d")
    f = f"pnl_logs/{d}.csv"
    os.makedirs("pnl_logs", exist_ok=True)
    write_header = not os.path.isfile(f)
    with open(f, 'a', newline='') as file:
        w = csv.writer(file)
        if write_header:
            w.writerow(['symbol', 'timestamp', 'profit_rm', 'balance_rm'])
        w.writerow([symbol, timestamp, profit_rm, balance_rm])
