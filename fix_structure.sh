#!/bin/bash

echo "[INFO] Mula susun struktur folder AlphaTango..."

# 1. Cipta folder jika belum wujud
mkdir -p executors scanner handlers streamers utils system scripts logs pnl_logs data legacy

# 2. Pindahkan fail ke folder berkaitan (jika belum di sana)
[ -f async_executor.py ] && mv async_executor.py executors/async_executor.py
[ -f simulator.py ] && mv simulator.py executors/simulation_executor.py
[ -f symbol_selector.py ] && mv symbol_selector.py scanner/
[ -f balance_handler.py ] && mv balance_handler.py handlers/
[ -f alphatelegram/handlers.py ] && cp alphatelegram/handlers.py handlers/telegram_handler.py
[ -f executors/price_streamer.py ] && mv executors/price_streamer.py streamers/
[ -f utils/latency_tracker.py ] && mv utils/latency_tracker.py streamers/

# 3. Tambah __init__.py dalam semua folder supaya boleh import sebagai modul
for dir in executors scanner handlers streamers utils system scripts logs pnl_logs data legacy; do
    touch $dir/__init__.py
done

echo "[INFO] Struktur projek telah dikemaskini dengan berjaya."
