import csv
import os
from datetime import datetime

def log_trade_to_csv(trade_data: dict, balance: float):
    date_str = datetime.now().strftime('%Y-%m-%d')
    filename = f"pnl_logs/{date_str}.csv"
    file_exists = os.path.isfile(filename)

    os.makedirs("pnl_logs", exist_ok=True)  # Pastikan folder wujud

    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['Time', 'Symbol', 'Profit(RM)', 'New Balance(RM)'])

        writer.writerow([
            datetime.now().strftime('%H:%M:%S'),
            trade_data.get("symbol", "UNKNOWN"),
            f"{trade_data.get('profit', 0):.2f}",
            f"{balance:.2f}"
        ])
