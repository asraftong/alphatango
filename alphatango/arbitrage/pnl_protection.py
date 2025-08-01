import csv
import os
import logging
from datetime import datetime

from config import Config
from telegram.alerts import send_error_alert  # ? Import dikemaskini ikut struktur baru


def log_trade_to_csv(symbol: str, profit_rm: float, balance_rm: float):
    """
    Log dagangan ke dalam fail CSV harian mengikut format:
    Timestamp, Symbol, Profit (RM), Balance (RM)
    """
    try:
        date_str = datetime.now().strftime("%Y-%m-%d")
        log_dir = Config.LOG_DIR_PNL if hasattr(Config, "LOG_DIR_PNL") else "pnl_logs"
        os.makedirs(log_dir, exist_ok=True)
        filename = os.path.join(log_dir, f"{date_str}.csv")
        file_exists = os.path.isfile(filename)

        with open(filename, mode="a", newline="") as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(["Timestamp", "Symbol", "Profit (RM)", "Balance (RM)"])
            writer.writerow([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                symbol,
                round(profit_rm, 2),
                round(balance_rm, 2),
            ])
    except Exception as e:
        logging.error(f"[PNL LOGGING] Gagal log PnL: {e}")
        try:
            send_error_alert(f"[PNL LOGGING] Gagal log PnL: {e}")
        except Exception as alert_err:
            logging.error(f"[PNL LOGGING] Gagal hantar alert Telegram: {alert_err}")


def is_pnl_within_threshold(profit: float) -> bool:
    """
    Semak sama ada profit semasa berada dalam julat dibenarkan.
    """
    return Config.PNL_THRESHOLD_MIN <= profit <= Config.PNL_THRESHOLD_MAX


def get_total_pnl() -> float:
    """
    Jumlahkan semua nilai 'Profit (RM)' daripada fail-fail CSV dalam folder pnl_logs.
    """
    total_pnl = 0.0
    log_dir = Config.LOG_DIR_PNL if hasattr(Config, "LOG_DIR_PNL") else "pnl_logs"

    try:
        if not os.path.isdir(log_dir):
            return 0.0

        for filename in os.listdir(log_dir):
            if filename.endswith(".csv"):
                filepath = os.path.join(log_dir, filename)
                with open(filepath, mode="r") as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        try:
                            total_pnl += float(row["Profit (RM)"])
                        except (ValueError, KeyError):
                            continue
    except Exception as e:
        logging.error(f"[PNL TOTAL] Gagal kira jumlah PnL: {e}")
        try:
            send_error_alert(f"[PNL TOTAL] Gagal kira jumlah PnL: {e}")
        except Exception as alert_err:
            logging.error(f"[PNL TOTAL] Gagal hantar alert Telegram: {alert_err}")
    
    return round(total_pnl, 2)
