import os
import asyncio
from dotenv import load_dotenv

load_dotenv()
LOG_FILE = '/opt/alphatango/log/alphatango.err.log'
LAST_LINE_FILE = '/opt/alphatango/log/.last_error_line'

TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

async def send_telegram(message):
    import aiohttp
    async with aiohttp.ClientSession() as session:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        await session.post(url, json={"chat_id": TELEGRAM_CHAT_ID, "text": message})

def read_last_line():
    try:
        with open(LAST_LINE_FILE, 'r') as f:
            return int(f.read().strip())
    except:
        return 0

def write_last_line(line_num):
    with open(LAST_LINE_FILE, 'w') as f:
        f.write(str(line_num))

async def main():
    if not os.path.exists(LOG_FILE):
        return
    last_line = read_last_line()
    with open(LOG_FILE, 'r') as f:
        lines = f.readlines()

    new_lines = lines[last_line:]
    errors = [line for line in new_lines if "ERROR" in line or "Exception" in line]

    if errors:
        await send_telegram(f"🚨 Log Monitor Detected Errors:\n{''.join(errors[-3:])[-300:]}")

    write_last_line(len(lines))

asyncio.run(main())
