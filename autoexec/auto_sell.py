# /opt/alphatango/autoexec/auto_sell.py

import csv
import os
import logging
import asyncio
from datetime import datetime
from config import Config
from alphatelegram.alerts import send_telegram_alert
from streamers.price_streamer import get_cached_price
from binance.client import Client
from dotenv import load_dotenv

load_dotenv()
client = Client(os.getenv("BINANCE_API_KEY"), os.getenv("BINANCE_API_SECRET"))

POSITIONS_FILE = "/opt/alphatango/data/open_positions.csv"

async def monitor_and_sell():
    while True:
        if not os.path.exists(POSITIONS_FILE):
            await asyncio.sleep(10)
            continue

        updated_positions = []

        with open(POSITIONS_FILE, "r") as f:
            reader = csv.DictReader(f)
            positions = list(reader)

        for pos in positions:
            symbol = pos["symbol"]
            buy_price = float(pos["buy_price"])
            quantity = float(pos["quantity"])
            buy_time = pos["buy_time"]

            current_price = get_cached_price(symbol)
            if current_price is None:
                continue

            profit_percent = ((current_price - buy_price) / buy_price) * 100

            if profit_percent >= 1.5:
                try:
                    # Hantar order jual sebenar
                    order = client.order_market_sell(symbol=symbol, quantity=quantity)

                    log_msg = f"[AUTO_SELL] Sold {quantity} {symbol} at {current_price:.5f} (Profit {profit_percent:.2f}%)"
                    logging.info(log_msg)
                    await send_telegram_alert(log_msg)

                    log_pnl_to_csv(symbol, buy_time, datetime.utcnow(), buy_price, current_price, quantity, profit_percent)

                    continue  # Skip simpan position ni (sudah dijual)

                except Exception as e:
                    logging.error(f"[AUTO_SELL] Gagal jual {symbol}: {e}")
                    await send_telegram_alert(f"❌ Gagal jual {symbol} ({quantity}) - {e}")
                    updated_positions.append(pos)
            else:
                updated_positions.append(pos)

        # Simpan balik yang belum dijual
        with open(POSITIONS_FILE, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["symbol", "buy_price", "quantity", "buy_time"])
            writer.writeheader()
            writer.writerows(updated_positions)

        await asyncio.sleep(5)  # Ulang setiap 5 saat


def log_pnl_to_csv(symbol, buy_time, sell_time, buy_price, sell_price, quantity, profit_percent):
    pnl_dir = "/opt/alphatango/pnl_logs"
    os.makedirs(pnl_dir, exist_ok=True)
    pnl_file = os.path.join(pnl_dir, f"{datetime.utcnow().date()}.csv")

    with open(pnl_file, "a", newline="") as f:
        writer = csv.writer(f)
        if f.tell() == 0:
            writer.writerow(["symbol", "buy_time", "sell_time", "buy_price", "sell_price", "quantity", "profit_%"])
        writer.writerow([
            symbol,
            buy_time,
            sell_time.strftime("%Y-%m-%d %H:%M:%S"),
            round(buy_price, 8),
            round(sell_price, 8),
            quantity,
            round(profit_percent, 2),
        ])
