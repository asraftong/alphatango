import logging
import time
import requests
from config import Config

# Cache untuk info simbol
symbol_info_cache = {}
cache_expiry = 60 * 60  # 1 jam cache

def get_symbol_info(symbol: str):
    symbol = symbol.upper()
    now = time.time()

    if symbol in symbol_info_cache:
        cached = symbol_info_cache[symbol]
        if now - cached["timestamp"] < cache_expiry:
            return cached["info"]

    try:
        url = f"{Config.BINANCE_API_BASE}/api/v3/exchangeInfo?symbol={symbol}"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()

        if "symbols" not in data or not data["symbols"]:
            raise ValueError(f"Tiada info untuk simbol {symbol}")

        info = data["symbols"][0]
        symbol_info_cache[symbol] = {
            "timestamp": now,
            "info": info,
        }
        return info

    except Exception as e:
        logging.warning(f"[EXCHANGE] Gagal ambil info simbol {symbol}: {e}")
        return {}

def extract_filters(info: dict):
    filters = {}
    try:
        for f in info.get("filters", []):
            filters[f["filterType"]] = f
    except Exception as e:
        logging.warning(f"[EXCHANGE] Gagal extract filters: {e}")
    return filters

def get_symbol_filters(symbol: str) -> dict:
    """
    Fungsi ini digunakan oleh live_executor.py
    untuk mendapatkan filter seperti LOT_SIZE dan MIN_NOTIONAL.
    """
    info = get_symbol_info(symbol)
    if not info:
        logging.warning(f"[EXCHANGE] Info simbol kosong untuk {symbol}")
        return {}
    return extract_filters(info)

def get_lot_size(symbol: str) -> float:
    filters = get_symbol_filters(symbol)
    try:
        return float(filters.get("LOT_SIZE", {}).get("stepSize", 0.0))
    except Exception as e:
        logging.warning(f"[EXCHANGE] Gagal dapatkan LOT_SIZE untuk {symbol}: {e}")
        return 0.0

def get_min_notional(symbol: str) -> float:
    filters = get_symbol_filters(symbol)
    try:
        return float(filters.get("MIN_NOTIONAL", {}).get("minNotional", 0.0))
    except Exception as e:
        logging.warning(f"[EXCHANGE] Gagal dapatkan MIN_NOTIONAL untuk {symbol}: {e}")
        return 0.0

def get_tick_size(symbol: str) -> float:
    filters = get_symbol_filters(symbol)
    try:
        return float(filters.get("PRICE_FILTER", {}).get("tickSize", 0.0))
    except Exception as e:
        logging.warning(f"[EXCHANGE] Gagal dapatkan TICK_SIZE untuk {symbol}: {e}")
        return 0.0
