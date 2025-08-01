import asyncio
import logging
from datetime import datetime
from decimal import Decimal, ROUND_DOWN
from binance import AsyncClient, exceptions
from config import Config
from alphatelegram.alerts import send_telegram_alert

async def convert_funds():
    client = None
    try:
        client = await AsyncClient.create(Config.BINANCE_API_KEY, Config.BINANCE_API_SECRET)
        account = await client.get_account()
        balances = {asset['asset']: float(asset['free']) for asset in account['balances']}

        bnb = balances.get("BNB", 0)
        doge = balances.get("DOGE", 0)

        logging.info(f"[CONVERT] BNB: {bnb}, DOGE: {doge}")

        orders = []

        # Convert DOGE to USDT (jika ada)
        if doge >= 1:
            doge_price = float((await client.get_symbol_ticker(symbol="DOGEUSDT"))['price'])
            qty_doge = str(Decimal(doge).quantize(Decimal('0.1'), rounding=ROUND_DOWN))

            order = await client.create_order(
                symbol="DOGEUSDT",
                side="SELL",
                type="MARKET",
                quantity=qty_doge
            )
            logging.info(f"[SELL] Jual {qty_doge} DOGE pada harga ~{doge_price} → USDT")
            orders.append(f"Jual {qty_doge} DOGE → USDT")

        # Convert 50% BNB to USDT
        if bnb >= 0.01:
            half_bnb = float(bnb) / 2
            qty_bnb = str(Decimal(half_bnb).quantize(Decimal('0.001'), rounding=ROUND_DOWN))
            bnb_price = float((await client.get_symbol_ticker(symbol="BNBUSDT"))['price'])

            order = await client.create_order(
                symbol="BNBUSDT",
                side="SELL",
                type="MARKET",
                quantity=qty_bnb
            )
            logging.info(f"[SELL] Jual {qty_bnb} BNB pada harga ~{bnb_price} → USDT")
            orders.append(f"Jual {qty_bnb} BNB → USDT")

        if not orders:
            msg = "[CONVERT] ❌ Tiada aset mencukupi untuk dijual."
            logging.warning(msg)
            await send_telegram_alert(msg)
        else:
            msg = "[CONVERT] ✅ Transaksi berjaya:\n" + "\n".join(orders)
            await send_telegram_alert(msg)

    except exceptions.BinanceAPIException as e:
        msg = f"[CONVERT] ❌ Binance API Error: {e}"
        logging.exception(msg)
        await send_telegram_alert(msg)
    except Exception as e:
        msg = f"[CONVERT] ❌ Ralat umum semasa convert: {e}"
        logging.exception(msg)
        await send_telegram_alert(msg)
    finally:
        if client:
            await client.close_connection()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(convert_funds())
