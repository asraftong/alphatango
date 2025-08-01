import logging
from config import Config
from alphatelegram.alerts import send_telegram_alert

async def get_symbols_for_arbitrage():
    try:
        selected_symbols = []
        for symbol in Config.SYMBOL_LIST:  # ✅ Nama betul ikut config.py
            if "USDT" in symbol:
                selected_symbols.append(symbol)

        if not selected_symbols:
            msg = "[SYMBOL SELECTOR] Tiada simbol layak ditemui untuk arbitrage."
            logging.warning(msg)
            await send_telegram_alert(msg)

        return selected_symbols

    except Exception as e:
        logging.error(f"[SYMBOL SELECTOR] Ralat semasa pemilihan simbol: {e}")
        try:
            await send_telegram_alert(f"[SYMBOL SELECTOR] Ralat: {e}")
        except Exception as alert_err:
            logging.error(f"[SYMBOL SELECTOR] Gagal hantar alert Telegram: {alert_err}")
        return []
