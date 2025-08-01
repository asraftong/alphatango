import json
import os
import logging
from binance.client import Client
from dotenv import load_dotenv
import asyncio
import aiohttp

# Load .env
load_dotenv()

# Setup logging dengan format DD:MM:YY
logging.basicConfig(
    filename='/opt/alphatango/log/update_symbol.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%d:%m:%y'
)

# Binance API
api_key = os.getenv("BINANCE_API_KEY")
api_secret = os.getenv("BINANCE_API_SECRET")
client = Client(api_key, api_secret)

# Telegram Config
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

async def send_telegram_alert(message: str):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        logging.warning("Telegram config not set. Skipping alert.")
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as resp:
                if resp.status != 200:
                    logging.warning(f"Telegram alert failed with status {resp.status}")
    except Exception as e:
        logging.error(f"Telegram alert error: {str(e)}")

def fetch_symbol_filters():
    exchange_info = client.get_exchange_info()
    symbols_data = {}

    for symbol_info in exchange_info['symbols']:
        symbol = symbol_info['symbol']
        filters = {f['filterType']: f for f in symbol_info['filters']}

        # Semak kewujudan dan kesahan kedua-dua filter
        if 'LOT_SIZE' not in filters or 'MIN_NOTIONAL' not in filters:
            continue
        if not filters['MIN_NOTIONAL'].get('minNotional'):
            continue

        symbols_data[symbol] = {
            'LOT_SIZE': filters['LOT_SIZE'],
            'MIN_NOTIONAL': filters['MIN_NOTIONAL']
        }

    with open('/opt/alphatango/symbol_filters.json', 'w') as f:
        json.dump(symbols_data, f, indent=2)

    logging.info(f"[UPDATE] Berjaya update symbol filters: {len(symbols_data)} simbol")

if __name__ == "__main__":
    try:
        fetch_symbol_filters()
    except Exception as e:
        error_msg = f"[ERROR] Gagal update symbol filters: {str(e)}"
        logging.error(error_msg)
        asyncio.run(send_telegram_alert(error_msg))
