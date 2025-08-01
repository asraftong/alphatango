import os
import shutil

BASE = "/opt/alphatango"

# Map asal -> destinasi
MIGRATION_MAP = {
    "telegram_handler.py": "alphatango/telegram/alerts.py",
    "handlers/telegram_handler.py": "alphatango/telegram/alerts.py",
    "alphaexec/live_executor.py": "alphatango/executors/live_executor.py",
    "alphaexec/simulation_executor.py": "alphatango/executors/simulation_executor.py",
    "alphaexec/async_executor.py": "alphatango/executors/async_executor.py",
    "exchange.py": "alphatango/exchange/binance_api.py",
    "price_streamer.py": "alphatango/exchange/price_streamer.py",
    "pnl_protection.py": "alphatango/arbitrage/pnl_protection.py",
    "arbitrage_logic.py": "alphatango/arbitrage/logic.py",
    "executor_selector.py": "alphatango/arbitrage/executor_selector.py",
    "symbol_selector.py": "alphatango/scanner/symbol_selector.py",
    "symbol_fetcher.py": "alphatango/scanner/symbol_fetcher.py",
    "symbol_filter.py": "alphatango/scanner/symbol_filter.py",
    "utils.py": "alphatango/utils/logger.py",
    "utils_async.py": "alphatango/utils/async_tools.py",
    "utils_binance.py": "alphatango/utils/binance_helpers.py",
    "pnl_logger.py": "alphatango/services/pnl_logger.py",
    "log_monitor.py": "alphatango/services/log_monitor.py",
    "balance_simulator.py": "alphatango/services/balance_simulator.py",
    "healthcheck.py": "alphatango/services/healthcheck.py",
}

# Folder yang perlu pastikan wujud + __init__.py
FOLDERS = [
    "alphatango",
    "alphatango/arbitrage",
    "alphatango/executors",
    "alphatango/exchange",
    "alphatango/telegram",
    "alphatango/scanner",
    "alphatango/utils",
    "alphatango/services",
]

def ensure_folders():
    for folder in FOLDERS:
        path = os.path.join(BASE, folder)
        os.makedirs(path, exist_ok=True)
        init_file = os.path.join(path, "__init__.py")
        if not os.path.exists(init_file):
            with open(init_file, "w") as f:
                f.write("# Auto-created\n")
    print("[✔] Semua folder dan __init__.py disediakan.")

def migrate_files():
    for old, new in MIGRATION_MAP.items():
        old_path = os.path.join(BASE, old)
        new_path = os.path.join(BASE, new)
        if os.path.exists(old_path):
            shutil.move(old_path, new_path)
            print(f"[→] {old} -> {new}")
        else:
            print(f"[⚠] SKIP: {old} tak jumpa")

def main():
    print("🚀 Memulakan migrasi struktur AlphaTango...")
    ensure_folders()
    migrate_files()
    print("✅ Migrasi selesai. Sila semak alphatango/ untuk struktur baru.")

if __name__ == "__main__":
    main()
