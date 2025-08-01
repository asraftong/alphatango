import datetime
import platform
from aiogram import types
from config import Config
from alphatelegram import state

# Optional: untuk uptime tracking
BOT_START_TIME = datetime.datetime.now()

async def handle_status_command(message: types.Message):
    now = datetime.datetime.now()
    uptime = now - BOT_START_TIME

    status_lines = [
        f"🤖 <b>Status Bot AlphaTango</b>",
        f"🕹 Mode: <code>{Config.MODE.upper()}</code>",
        f"🔕 Alerts Muted: <code>{state.alerts_muted}</code>",
        f"🕒 Uptime: <code>{str(uptime).split('.')[0]}</code>",
        f"💻 Host: <code>{platform.node()}</code>",
    ]

    # Optional tambahan jika mahu
    if hasattr(state, "last_binance_connection"):
        last_conn = state.last_binance_connection.strftime("%Y-%m-%d %H:%M:%S")
        status_lines.append(f"📡 Binance Last Ping: <code>{last_conn}</code>")

    await message.answer("\n".join(status_lines), parse_mode="HTML")
