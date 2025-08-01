import logging
import os
import json
from datetime import datetime

# Fail simpanan posisi terbuka
POSITION_FILE = "/opt/alphatango/data/open_positions.json"

def round_step_size(quantity, step_size):
    """
    Pembundaran ikut stepSize (LOT_SIZE).
    """
    precision = int(round(-1 * (len(str(step_size).split(".")[1]))))
    return round(quantity, precision)

def calculate_trade_amount(balance, percentage=0.99):
    """
    Kira nilai trade ikut % daripada baki tersedia.
    """
    return balance * percentage

def format_symbol(symbol: str) -> str:
    """
    Format simbol jadi bentuk standard Binance.
    """
    return symbol.replace("/", "").upper()

def log_trade_to_csv(symbol, side, price, quantity, profit_rm, balance_rm):
    """
    Log trade ke dalam fail CSV harian.
    """
    date_str = datetime.now().strftime("%Y-%m-%d")
    log_dir = f"/opt/alphatango/pnl_logs"
    os.makedirs(log_dir, exist_ok=True)
    filename = f"{log_dir}/{date_str}.csv"

    row = f"{datetime.now()},{symbol},{side},{price},{quantity},{profit_rm:.2f},{balance_rm:.2f}\n"

    try:
        write_header = not os.path.exists(filename)
        with open(filename, "a") as f:
            if write_header:
                f.write("timestamp,symbol,side,price,quantity,profit_rm,balance_rm\n")
            f.write(row)
    except Exception as e:
        logging.error(f"[UTILS] Gagal tulis log trade ke CSV: {e}")

def save_open_position(position):
    """
    Simpan posisi terbuka ke fail JSON.
    """
    os.makedirs(os.path.dirname(POSITION_FILE), exist_ok=True)
    try:
        if os.path.exists(POSITION_FILE):
            with open(POSITION_FILE, 'r') as f:
                data = json.load(f)
        else:
            data = {}

        symbol = position['symbol']
        data[symbol] = position

        with open(POSITION_FILE, 'w') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        logging.error(f"[UTILS] Gagal simpan posisi terbuka: {e}")

def load_open_positions():
    """
    Baca semua posisi terbuka dari fail.
    """
    try:
        if os.path.exists(POSITION_FILE):
            with open(POSITION_FILE, 'r') as f:
                return json.load(f)
        return {}
    except Exception as e:
        logging.error(f"[UTILS] Gagal baca fail posisi terbuka: {e}")
        return {}

def remove_open_position(symbol):
    """
    Padam posisi selepas jualan.
    """
    try:
        if os.path.exists(POSITION_FILE):
            with open(POSITION_FILE, 'r') as f:
                data = json.load(f)
            if symbol in data:
                del data[symbol]
                with open(POSITION_FILE, 'w') as f:
                    json.dump(data, f, indent=4)
    except Exception as e:
        logging.error(f"[UTILS] Gagal padam posisi untuk {symbol}: {e}")
