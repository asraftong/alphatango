#!/bin/bash

echo "Memulakan AlphaTango dalam LIVE mode..."

# Lokasi projek
PROJECT_DIR="/opt/alphatango"
LOG_DIR="$PROJECT_DIR/log"
LOG_FILE="$LOG_DIR/live_start.log"

# Aktifkan virtualenv
source "$PROJECT_DIR/venv/bin/activate"

# Hantar alert Telegram (melalui skrip Python inline)
echo "[INFO] Menghantar alert Telegram permulaan..."
python3 <<EOF
import os
from dotenv import load_dotenv
import requests

load_dotenv("$PROJECT_DIR/.env")

token = os.getenv("TELEGRAM_BOT_TOKEN")
chat_id = os.getenv("TELEGRAM_CHAT_ID")
msg = "🚀 AlphaTango telah dimulakan dalam LIVE mode.\nSila pantau log untuk sebarang tindakan lanjut."

if token and chat_id:
    try:
        requests.post(f"https://api.telegram.org/bot{token}/sendMessage", data={
            "chat_id": chat_id,
            "text": msg
        })
        print("[INFO] Alert Telegram dihantar.")
    except Exception as e:
        print(f"[ERROR] Gagal hantar alert: {e}")
else:
    print("[ERROR] Konfigurasi Telegram tidak lengkap!")
EOF

# Log permulaan
echo "[START] LIVE start: $(date '+%Y-%m-%d %H:%M:%S')" >> "$LOG_FILE"

# Jalankan bot
echo "[INFO] Menjalankan main.py dalam mod LIVE..."
cd "$PROJECT_DIR"
python3 main.py >> "$LOG_DIR/alphatango_live.log" 2>&1
