import logging
import aiohttp
import os
import csv
from datetime import datetime
from aiogram import Router, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from config import Config

# ========== ALERT SYSTEM ==========

async def send_telegram_alert(message: str):
    from .commands import is_muted  # elak circular import

    if is_muted() and not any(kw in message for kw in ["Ralat", "Fatal", "❌", "‼️", "⚠️"]):
        return

    url = f"https://api.telegram.org/bot{Config.TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": Config.TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as resp:
                if resp.status != 200:
                    logging.warning(f"[TELEGRAM] Gagal hantar mesej: {await resp.text()}")
    except Exception as e:
        logging.exception(f"[TELEGRAM] Gagal hantar alert: {e}")

# ========== ROUTER ==========

router = Router()

@router.message(Command("mute"))
async def mute_handler(message: Message):
    from .commands import handle_mute
    await handle_mute(message)

@router.message(Command("unmute"))
async def unmute_handler(message: Message):
    from .commands import handle_unmute
    await handle_unmute(message)

@router.message(Command("status"))
async def status_handler(message: Message):
    from .commands import handle_status
    await handle_status(message)

@router.message(Command("symbols"))
async def symbols_handler(message: Message):
    from scanner.symbol_selector import get_symbols_for_arbitrage
    try:
        symbols = await get_symbols_for_arbitrage()
        if symbols:
            await message.answer(f"✅ Simbol aktif:\n<code>{', '.join(symbols)}</code>", parse_mode="HTML")
        else:
            await message.answer("⚠️ Tiada simbol layak buat masa ini.")
    except Exception as e:
        await message.answer(f"❌ Ralat semasa ambil simbol:\n<code>{e}</code>", parse_mode="HTML")

@router.message(Command("pnl"))
async def pnl_handler(message: Message):
    today = datetime.now().strftime("%Y-%m-%d")
    filepath = os.path.join(Config.PNL_LOG_DIR, f"{today}.csv")

    if not os.path.exists(filepath):
        await message.answer("📂 Tiada rekod PnL untuk hari ini.")
        return

    try:
        total = 0
        trades = []
        with open(filepath, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                profit = float(row["profit_rm"])
                total += profit
                trades.append(f"{row['time']} {row['symbol']}: {profit:.2f} RM")

        reply = "📊 <b>PNL Hari Ini</b>\n" + "\n".join(trades[-5:])
        reply += f"\n\n<b>Jumlah:</b> {total:.2f} RM"
        await message.answer(reply, parse_mode="HTML")
    except Exception as e:
        await message.answer(f"❌ Ralat semasa baca PnL:\n<code>{e}</code>", parse_mode="HTML")

@router.message(Command("help"))
async def help_handler(message: Message):
    help_text = (
        "📘 <b>Senarai Perintah Tersedia:</b>\n\n"
        "/status - Status semasa sistem\n"
        "/mute - Senyapkan alert biasa\n"
        "/unmute - Aktifkan alert semula\n"
        "/symbols - Simbol layak untuk arbitrage\n"
        "/pnl - Ringkasan keuntungan hari ini\n"
        "/help - Bantuan\n"
    )
    await message.answer(help_text, parse_mode="HTML")

# Fallback untuk mesej tak dikenali
@router.message()
async def unknown_command(message: Message):
    await message.answer(f"❓ Perintah tidak dikenali:\n<code>{message.text}</code>", parse_mode="HTML")

# ========== REGISTER ALL ==========

def register_handlers(dispatcher: Dispatcher):
    dispatcher.include_router(router)
