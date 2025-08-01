import asyncio
import logging
import os
import signal
import json
from datetime import datetime
from dotenv import load_dotenv

from alphatango.config.base import Config
from alphatango.telegram.alerts import send_telegram_alert
from alphatango.telegram.bot import register_handlers

os.chdir("/opt/alphatango")
load_dotenv()

os.makedirs("logs", exist_ok=True)
log_file = os.path.join("logs", f"alphatango_{Config.MODE.lower()}.log")

class CustomFormatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        dt = datetime.fromtimestamp(record.created)
        return dt.strftime("%d:%m:%Y %H:%M:%S")

formatter = CustomFormatter("%(asctime)s [%(levelname)s] %(message)s")
logging.basicConfig(
    level=logging.INFO,
    handlers=[logging.FileHandler(log_file), logging.StreamHandler()]
)
for handler in logging.getLogger().handlers:
    handler.setFormatter(formatter)

logging.info(f"[STARTUP] Memulakan AlphaTango dalam mode {Config.MODE}...")

Executor = None
start_price_stream = None
get_symbols_for_arbitrage = None

try:
    if Config.MODE == "SIMULATION":
        from alphatango.execution.async_executor import AsyncExecutor as Executor
    elif Config.MODE == "LIVE":
        from alphatango.execution.live_executor import LiveExecutor as Executor
        from alphatango.exchange.websocket import start_price_stream
        from alphatango.arbitrage.selector import get_symbols_for_arbitrage
    else:
        raise ValueError(f"MODE tidak dikenali: {Config.MODE}")
except ImportError as e:
    logging.exception(f"[IMPORT ERROR] {e}")
    asyncio.run(send_telegram_alert(f"🚨 Gagal import modul penting:\n<code>{e}</code>"))
    raise

stop_flag = asyncio.Event()

def handle_signal(signame):
    logging.warning(f"[SIGNAL] Menerima signal {signame}. Shutdown disediakan...")
    stop_flag.set()

for sig in ('SIGINT', 'SIGTERM'):
    signal.signal(getattr(signal, sig), lambda signum, frame, s=sig: handle_signal(s))

async def arbitrage_main_loop():
    from alphatango.arbitrage.selector import get_arbitrage_opportunity

    if Config.MODE == "LIVE":
        eligible_symbols = []
        cache_file = os.path.join("data", "eligible_symbols.json")

        if os.path.exists(cache_file):
            try:
                with open(cache_file, "r") as f:
                    eligible_symbols = json.load(f)
                logging.info(f"[CACHE] 📦 Muatkan {len(eligible_symbols)} simbol dari cache.")
            except Exception as e:
                logging.warning(f"[CACHE] ⚠️ Gagal baca cache: {e}")

        if not eligible_symbols:
            eligible_symbols = await get_symbols_for_arbitrage()
            if not eligible_symbols:
                msg = "🚫 Tiada simbol layak untuk LIVE selepas fetch."
                logging.warning(f"[LIVE] {msg}")
                await send_telegram_alert(msg)
                return

            try:
                os.makedirs("data", exist_ok=True)
                with open(cache_file, "w") as f:
                    json.dump(eligible_symbols, f)
                logging.info(f"[CACHE] ✅ Simpan {len(eligible_symbols)} simbol ke cache.")
            except Exception as e:
                logging.warning(f"[CACHE ERROR] ❌ Gagal simpan cache: {e}")

        Config.SYMBOL_LIST = eligible_symbols
        asyncio.ensure_future(start_price_stream(eligible_symbols))

    executor = Executor()
    logging.info(f"[SYSTEM] ✅ AlphaTango dimulakan dalam mode {Config.MODE}")
    await send_telegram_alert(f"🚀 AlphaTango dimulakan dalam <b>{Config.MODE}</b> mode.")

    while not stop_flag.is_set():
        try:
            opportunity = await get_arbitrage_opportunity()
            if opportunity:
                symbol = opportunity["symbol"]
                base = opportunity["base"]
                quote = opportunity["quote"]
                profit = opportunity["profit_rm"]

                logging.info(f"[OPPORTUNITY] {symbol} | Base: {base} | Quote: {quote} | Profit: RM{profit:.4f}")
                await executor.execute_trade(opportunity)

            await asyncio.sleep(Config.SCAN_INTERVAL)

        except asyncio.CancelledError:
            logging.info("[LOOP] 🔁 Loop arbitrage dibatalkan.")
            break
        except Exception as e:
            msg = f"[MAIN LOOP ERROR] {type(e).__name__}: {e}"
            logging.exception(msg)
            await send_telegram_alert(f"🔥 Ralat dalam loop utama:\n<code>{msg}</code>")
            await asyncio.sleep(5)

async def combined_main():
    from aiogram import Bot, Dispatcher
    from aiogram.client.default import DefaultBotProperties

    bot = Bot(token=Config.TELEGRAM_BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
    dp = Dispatcher()
    register_handlers(dp)

    logging.info("[TELEGRAM] 🤖 Telegram bot dimulakan...")

    try:
        await asyncio.gather(
            dp.start_polling(bot),
            arbitrage_main_loop(),
            stop_flag.wait()
        )
    except asyncio.CancelledError:
        logging.warning("[SHUTDOWN] 🧯 Shutdown async digesa.")
    finally:
        logging.warning("[SHUTDOWN] Menutup bot dan sambungan...")
        await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(combined_main())
    except KeyboardInterrupt:
        logging.warning("[INTERRUPT] 👋 Keyboard interrupt dikesan. Keluar...")
    except Exception as e:
        logging.exception(f"[FATAL MAIN] {e}")
        try:
            asyncio.run(send_telegram_alert(f"💥 Fatal error dalam main.py:\n<code>{e}</code>"))
        except:
            pass
