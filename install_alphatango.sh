#!/bin/bash

echo "🚀 Memasang AlphaTango Arbitrage Bot..."

# 1. Kemas kini dan pasang keperluan sistem
sudo apt update && sudo apt upgrade -y
sudo apt install python3 python3-venv python3-pip git unzip -y

# 2. Buat direktori projek
mkdir -p /opt/alphatango
cd /opt/alphatango

# 3. Buat virtual environment
python3 -m venv venv
source venv/bin/activate

# 4. Salin fail requirements.txt
cat <<EOF > requirements.txt
aiohttp
websockets
python-telegram-bot==20.3
python-dotenv
ccxt
pandas
numpy
EOF

# 5. Pasang semua requirements
pip install --upgrade pip
pip install -r requirements.txt

# 6. Cipta direktori asas
mkdir -p logs modules configs

# 7. Tambah .env.example
cat <<EOF > .env.example
BINANCE_API_KEY=your_api_key_here
BINANCE_API_SECRET=your_api_secret_here
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_chat_id
EOF

# 8. Permissions
chmod -R 755 /opt/alphatango

echo "✅ Siap! Projek AlphaTango telah disediakan di /opt/alphatango"
echo "👉 Tukar nama .env.example kepada .env dan isikan maklumat API anda"
