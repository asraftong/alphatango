# /opt/alphatango/auto_sell.py

import asyncio
import csv
import logging
from datetime import datetime
from decimal import Decimal
from price_streamer import price_cache
from live_executor import sell_order
from alphatelegram.alerts import send_telegram_alert

BUY_LOG = "/opt/alphatango/log/live_buy_log.csv"
SELL_LOG = "/opt/alphatango/log/live_sell_log.csv"
PROFIT_TARGET = 0.015  # 1.5%

# Setup logging
logging.basicConfig(
    filename='/opt/alphatango/log/auto_sell.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

async def monitor_open_positions():
    seen = set()  # Elak jual dua kali

    while True:
        try:
            with open(BUY_LOG, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    symbol = row['symbol']
                    buy_price = Decimal(row['buy_price'])
                    quantity = Decimal(row['quantity'])
                    key = f"{symbol}_{buy_price}_{quantity}"

                    if key in seen:
                        continue

                    # Semak harga semasa
                    current_price = price_cache.get(symbol)
                    if not current_price:
                        continue

                    current_price = Decimal(str(current_price))
                    profit_pct = (current_price - buy_price) / buy_price

                    if profit_pct >= Decimal(PROFIT_TARGET):
                        result = await sell_order(symbol, float(quantity))
                        if not result:
                            logging.error(f"Gagal jual {symbol}. Hasil kosong.")
                            continue

                        sell_price = result['sell_price']
                        pnl = (sell_price - float(buy_price)) * float(quantity)
                        pnl = round(pnl, 2)

                        # Log ke SELL_LOG
                        with open(SELL_LOG, 'a', newline='') as sf:
                            writer = csv.writer(sf)
                            writer.writerow([
                                datetime.now().strftime("%d:%m:%Y %H:%M:%S"),
                                symbol,
                                float(buy_price),
                                sell_price,
                                float(quantity),
                                pnl
                            ])

                        # Telegram Alert
                        await send_telegram_alert(
                            f"?? Auto SELL {symbol}\n"
                            f"?? Beli: {buy_price}\n"
                            f"?? Jual: {sell_price}\n"
                            f"?? Untung: RM{pnl:.2f}"
                        )

                        logging.info(f"Auto sold {symbol} at {sell_price} (PnL RM{pnl:.2f})")
                        seen.add(key)

        except Exception as e:
            logging.error(f"Ralat semasa monitor: {e}")
            await send_telegram_alert(f"? Ralat dalam auto_sell.py: {e}")

        await asyncio.sleep(10)  # Tunggu 10s sebelum semak semula
