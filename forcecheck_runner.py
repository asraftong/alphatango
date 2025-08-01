import csv
import os
import logging
from datetime import datetime, timedelta
from alphatelegram.alerts import send_telegram_alert

PURCHASED_FILE = "/opt/alphatango/purchased_coins.csv"
FORCECHECK_LOG = "/opt/alphatango/log/forcecheck.log"

# Setup logging
logging.basicConfig(
    filename=FORCECHECK_LOG,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%d:%m:%Y %H:%M:%S'
)

FORCE_SELL_THRESHOLD_MINUTES = 15  # Jika lebih dari ini, dianggap stuck

def read_purchased_data():
    """
    Baca data purchased dari fail CSV.
    Pulangkan sebagai list of dict.
    """
    if not os.path.exists(PURCHASED_FILE):
        return []

    data = []
    try:
        with open(PURCHASED_FILE, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append(row)
    except Exception as e:
        logging.error(f"[FORCECHECK] ?? Gagal baca {PURCHASED_FILE}: {e}")
    return data

def parse_time(dt_string):
    try:
        return datetime.strptime(dt_string, "%d:%m:%Y %H:%M:%S")
    except Exception as e:
        logging.warning(f"[FORCECHECK] Format masa salah: {dt_string}")
        return None

def check_for_stuck_orders():
    now = datetime.now()
    stuck = []

    purchased = read_purchased_data()
    for row in purchased:
        symbol = row.get("symbol", "??").upper()
        time_str = row.get("buy_time", "")
        buy_time = parse_time(time_str)
        if not buy_time:
            continue

        elapsed = (now - buy_time).total_seconds() / 60  # dalam minit
        if elapsed > FORCE_SELL_THRESHOLD_MINUTES:
            stuck.append((symbol, int(elapsed)))

    return stuck

def forcecheck_main():
    stuck_orders = check_for_stuck_orders()
    if not stuck_orders:
        logging.info("[FORCECHECK] ? Tiada simbol stuck")
        return

    for symbol, minutes in stuck_orders:
        msg = f"?? FORCECHECK: {symbol} telah dibeli {minutes} minit lalu dan masih belum dijual."
        logging.warning(msg)
        send_telegram_alert(msg)
        # Di masa hadapan boleh tambah fungsi auto-sell paksa di sini

if __name__ == "__main__":
    forcecheck_main()
