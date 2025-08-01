from aiogram import types
from alphatelegram import state

async def handle_mute_command(message: types.Message):
    state.alerts_muted = True
    await message.answer("🔕 Alert telah dimatikan.")
