from aiogram import types
from alphatelegram import state

async def handle_unmute_command(message: types.Message):
    state.alerts_muted = False
    await message.answer("🔔 Alert telah diaktifkan semula.")
