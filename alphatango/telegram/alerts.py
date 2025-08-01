# /opt/alphatango/alphatelegram/alerts.py

import aiohttp
import asyncio
import logging
from config import Config

async def send_telegram_alert(message: str):
    """
    Hantar mesej ke Telegram secara async.
    Boleh digunakan oleh mana-mana modul dalam sistem secara async.
    """
    if not getattr(Config, "TELEGRAM_ENABLED", True):
        logging.info("[TELEGRAM] Penghantaran mesej dinyahaktifkan (TELEGRAM_ENABLED=False).")
        return

    url = f"https://api.telegram.org/bot{Config.TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": Config.TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=payload) as resp:
                if resp.status != 200:
                    response_text = await resp.text()
                    logging.error(f"[TELEGRAM] Gagal hantar mesej. Status: {resp.status}, Response: {response_text}")
                else:
                    logging.info("[TELEGRAM] Mesej berjaya dihantar.")
    except Exception as e:
        logging.exception(f"[TELEGRAM] Ralat semasa hantar mesej: {e}")

def send_telegram_message(message: str):
    """
    Hantar mesej Telegram dari kod bukan-async (sync).
    Akan jalankan fungsi async secara automatik.
    Sesuai digunakan dalam skrip atau error handler biasa.
    """
    try:
        # Untuk persekitaran tanpa event loop aktif
        asyncio.run(send_telegram_alert(message))
    except RuntimeError:
        # Jika sudah dalam event loop (contohnya FastAPI atau main async)
        loop = asyncio.get_event_loop()
        loop.create_task(send_telegram_alert(message))
