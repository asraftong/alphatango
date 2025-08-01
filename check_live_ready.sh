#!/bin/bash

echo "===== AlphaTango LIVE Mode Checklist ====="

# Semak .env wujud
if [ ! -f "/opt/alphatango/.env" ]; then
    echo "[❌] Fail .env tidak wujud!"
    exit 1
fi

# Semak MODE
MODE=$(grep "^MODE=" /opt/alphatango/.env | cut -d '=' -f2 | tr -d '[:space:]')
if [ "$MODE" != "LIVE" ]; then
    echo "[⚠️ ] MODE bukan LIVE. Sekarang: $MODE"
else
    echo "[✅] MODE diset ke LIVE"
fi

# Semak API Key & Secret
API_KEY=$(grep "^BINANCE_API_KEY=" /opt/alphatango/.env | cut -d '=' -f2)
API_SECRET=$(grep "^BINANCE_API_SECRET=" /opt/alphatango/.env | cut -d '=' -f2)
if [ -z "$API_KEY" ] || [ -z "$API_SECRET" ]; then
    echo "[❌] BINANCE_API_KEY atau SECRET kosong!"
else
    echo "[✅] Kunci Binance tersedia"
fi

# Semak Telegram Bot
TELEGRAM_TOKEN=$(grep "^TELEGRAM_BOT_TOKEN=" /opt/alphatango/.env | cut -d '=' -f2)
TELEGRAM_CHAT_ID=$(grep "^TELEGRAM_CHAT_ID=" /opt/alphatango/.env | cut -d '=' -f2)
if [ -z "$TELEGRAM_TOKEN" ] || [ -z "$TELEGRAM_CHAT_ID" ]; then
    echo "[❌] Telegram Token atau Chat ID kosong!"
else
    echo "[✅] Konfigurasi Telegram lengkap"
fi

# Semak Baki USDT
echo -n "[⏳] Semak baki USDT Binance... "
source /opt/alphatango/venv/bin/activate
python3 <<EOF
from binance.client import Client
import os
from dotenv import load_dotenv

load_dotenv("/opt/alphatango/.env")
api_key = os.getenv("BINANCE_API_KEY")
api_secret = os.getenv("BINANCE_API_SECRET")

if not api_key or not api_secret:
    print("❌ API tidak sah!")
else:
    try:
        client = Client(api_key, api_secret)
        balance = client.get_asset_balance(asset='USDT')
        if balance and float(balance['free']) > 0:
            print(f"✅ Baki USDT: {balance['free']}")
        else:
            print("⚠️ Baki USDT kosong atau tidak ditemui")
    except Exception as e:
        print(f"❌ Ralat semak baki: {e}")
EOF

echo "==========================================="
echo "✅ Sedia untuk LIVE jika tiada [❌] di atas."
