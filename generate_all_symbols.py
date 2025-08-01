import os
import json
from binance.client import Client
from dotenv import load_dotenv

load_dotenv()

client = Client(api_key=os.getenv("BINANCE_API_KEY"), api_secret=os.getenv("BINANCE_API_SECRET"))

def fetch_all_symbols():
    exchange_info = client.get_exchange_info()
    usdt_symbols = []
    for symbol_info in exchange_info['symbols']:
        if symbol_info['status'] == 'TRADING' and symbol_info['quoteAsset'] == 'USDT':
            usdt_symbols.append(symbol_info['symbol'])
    return usdt_symbols

if __name__ == "__main__":
    all_symbols = fetch_all_symbols()

    os.makedirs("data", exist_ok=True)
    with open("data/all_symbols.json", "w") as f:
        json.dump(all_symbols, f, indent=2)

    print(f"{len(all_symbols)} simbol berjaya disimpan ke data/all_symbols.json")
