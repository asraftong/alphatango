import os
from dotenv import load_dotenv
import requests

load_dotenv("/opt/alphatango/.env")

token = os.getenv("TELEGRAM_BOT_TOKEN")
chat_id = os.getenv("TELEGRAM_CHAT_ID")
msg = " ^=^z  AlphaTango telah dimulakan dalam LIVE mode.\nSila pantau log untuk tindakan susulan."

if token and chat_id:
    try:
        requests.post(f"https://api.telegram.org/bot{token}/sendMessage", data={
            "chat_id": chat_id,
            "text": msg
        })
        print("[ ^|^e] Alert Telegram dihantar.")
    except Exception as e:
        print(f"[ ^}^l] Gagal hantar alert: {e}")
else:
    print("[ ^}^l] Konfigurasi Telegram tidak lengkap!")
