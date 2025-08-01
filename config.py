import os
import logging
from dotenv import load_dotenv

# === Muatkan .env dari direktori root projek ===
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.join(ROOT_DIR, ".env")
load_dotenv(ENV_PATH)

class Config:
    # === API Binance ===
    BINANCE_API_KEY = os.getenv("BINANCE_API_KEY", "").strip()
    BINANCE_API_SECRET = os.getenv("BINANCE_API_SECRET", "").strip()

    # === Telegram ===
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
    TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "").strip()

    # === Mod Operasi ===
    MODE = os.getenv("MODE", "SIMULATION").strip().upper()
    if MODE not in ("SIMULATION", "LIVE"):
        raise ValueError("[CONFIG] Config.MODE mesti sama ada 'SIMULATION' atau 'LIVE'.")

    # === Parameter Simulasi ===
    INITIAL_BALANCE_USDT = float(os.getenv("INITIAL_BALANCE_USDT", "1000"))
    INITIAL_BALANCE_BUSD = float(os.getenv("INITIAL_BALANCE_BUSD", "1000"))
    STARTING_BALANCE = INITIAL_BALANCE_USDT

    # === Parameter Sistem Umum ===
    QUOTE_CURRENCY = os.getenv("QUOTE_CURRENCY", "USDT").strip().upper()
    PRICE_CHECK_INTERVAL = float(os.getenv("PRICE_CHECK_INTERVAL", "1.0"))
    SCAN_INTERVAL = float(os.getenv("SCAN_INTERVAL", "5.0"))
    PROFIT_THRESHOLD = float(os.getenv("PROFIT_THRESHOLD", "0.2"))

    # === LIVE Mode: Saiz dagangan ===
    LIVE_TRADE_USDT = float(os.getenv("LIVE_TRADE_USDT", "2.00"))

    # === Auto-Sell ===
    AUTO_SELL_ENABLED = os.getenv("AUTO_SELL_ENABLED", "true").lower() == "true"
    AUTO_SELL_THRESHOLD = float(os.getenv("AUTO_SELL_THRESHOLD", "1.5"))

    # === Binance WebSocket ===
    BINANCE_WS_BASE = "wss://stream.binance.com:9443"

    # === Harga real-time ===
    SYMBOLS_TO_TRACK = os.getenv("SYMBOLS_TO_TRACK", "BTCUSDT,ETHUSDT,BNBUSDT")
    SYMBOLS_TO_TRACK = [
        sym.strip().upper() for sym in SYMBOLS_TO_TRACK.split(",") if sym.strip()
    ]

    # === Scanner utama ===
    SYMBOL_LIST = [
        "BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "ADAUSDT", "XRPUSDT", "DOGEUSDT",
        "MATICUSDT", "DOTUSDT", "AVAXUSDT", "SHIBUSDT", "LTCUSDT"
    ]

    # === Lokasi log ===
    LOG_DIR = os.getenv("LOG_DIR", "/opt/alphatango/log")
    PNL_LOG_DIR = os.getenv("PNL_LOG_DIR", "/opt/alphatango/pnl_logs")

    # === Format masa ===
    LOG_DATETIME_FORMAT = "%d:%m:%Y %H:%M:%S"

    # === Tetapan tambahan ===
    ENABLE_LATENCY_TRACKING = os.getenv("ENABLE_LATENCY_TRACKING", "true").lower() == "true"
    ENABLE_TELEGRAM_ALERTS = os.getenv("ENABLE_TELEGRAM_ALERTS", "true").lower() == "true"
    USE_EMOJI = os.getenv("USE_EMOJI", "true").lower() == "true"

    # === Validasi LIVE ===
    if MODE == "LIVE":
        missing = []
        if not BINANCE_API_KEY:
            missing.append("BINANCE_API_KEY")
        if not BINANCE_API_SECRET:
            missing.append("BINANCE_API_SECRET")
        if not TELEGRAM_BOT_TOKEN:
            missing.append("TELEGRAM_BOT_TOKEN")
        if not TELEGRAM_CHAT_ID:
            missing.append("TELEGRAM_CHAT_ID")
        if LIVE_TRADE_USDT <= 0:
            raise ValueError("[CONFIG] Nilai LIVE_TRADE_USDT mesti lebih dari 0.")
        if missing:
            raise ValueError(f"[CONFIG] Mod LIVE memerlukan .env mengandungi: {', '.join(missing)}")

    # === Amaran untuk SIMULATION jika token/chat id kosong ===
    if MODE == "SIMULATION":
        if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
            logging.warning("[CONFIG] TELEGRAM_BOT_TOKEN atau TELEGRAM_CHAT_ID tidak ditetapkan. Mesej Telegram mungkin tidak dihantar.")

# === Log ringkasan config ke log utama ===
if __name__ == "__main__" or True:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt=Config.LOG_DATETIME_FORMAT
    )
    logging.info("[CONFIG SUMMARY]")
    logging.info(f"MODE: {Config.MODE}")
    logging.info(f"LIVE_TRADE_USDT: {Config.LIVE_TRADE_USDT}")
    logging.info(f"PROFIT_THRESHOLD: {Config.PROFIT_THRESHOLD}")
    logging.info(f"QUOTE_CURRENCY: {Config.QUOTE_CURRENCY}")
    logging.info(f"SYMBOL_LIST: {Config.SYMBOL_LIST}")
    logging.info(f"SYMBOLS_TO_TRACK (LIVE WS): {Config.SYMBOLS_TO_TRACK}")
    logging.info(f"AUTO_SELL_ENABLED: {Config.AUTO_SELL_ENABLED}, THRESHOLD: {Config.AUTO_SELL_THRESHOLD}")
    logging.info(f"ENABLE_LATENCY_TRACKING: {Config.ENABLE_LATENCY_TRACKING}")
    logging.info(f"LOG_DIR: {Config.LOG_DIR}")
    logging.info(f"PNL_LOG_DIR: {Config.PNL_LOG_DIR}")
