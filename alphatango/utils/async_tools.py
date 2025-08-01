import asyncio
import logging
from binance import AsyncClient
from alphatelegram.handlers import send_telegram_alert

async def get_order_books_for_symbols(client: AsyncClient, symbols: list):
    """
    Ambil order book (buku pesanan) untuk senarai simbol secara asynchronous
    menggunakan Binance AsyncClient.

    Args:
        client (AsyncClient): Instance Binance AsyncClient.
        symbols (list): Senarai simbol (contoh: ["BTCUSDT", "ETHUSDT"]).

    Returns:
        dict: Dictionary simbol sebagai key, dan order book dict sebagai value.
    """
    try:
        tasks = [client.get_order_book(symbol=symbol) for symbol in symbols]
        order_books = await asyncio.gather(*tasks, return_exceptions=True)

        results = {}
        for symbol, result in zip(symbols, order_books):
            if isinstance(result, Exception):
                logging.error(f"[ORDER BOOK] Gagal dapat order book untuk {symbol}: {result}")
                continue
            results[symbol] = result

        return results
    except Exception as e:
        logging.error(f"[ERROR] get_order_books_for_symbols: {e}")
        return {}

async def get_balance(client: AsyncClient, asset: str) -> float:
    try:
        info = await client.get_asset_balance(asset=asset)
        if info is None or "free" not in info:
            return 0.0
        return float(info['free'])
    except Exception as e:
        logging.error(f"[BALANCE] Gagal dapatkan baki {asset}: {e}")
        return 0.0

async def place_market_order(client: AsyncClient, symbol: str, side: str, quantity: float):
    try:
        order = await client.create_order(
            symbol=symbol,
            side=side,
            type="MARKET",
            quantity=quantity
        )
        return order
    except Exception as e:
        await send_telegram_alert(f"? Gagal buat order {side} {symbol}: {e}")
        raise e

async def convert_max_bnb_to_usdt(retain_percent=40.0):
    """
    Tukar maksimum BNB ke USDT kecuali simpan baki retain_percent (contoh: 40%).

    Args:
        retain_percent (float): Peratus baki BNB yang hendak disimpan.

    Log Telegram dan juga log console.
    """
    try:
        client = await AsyncClient.create(
            api_key=None,  # Otomatik ambil dari env
            api_secret=None
        )

        bnb_balance = await get_balance(client, 'BNB')
        retained = bnb_balance * retain_percent / 100
        amount_to_convert = bnb_balance - retained

        if amount_to_convert < 0.01:
            await send_telegram_alert(f"? Gagal: baki BNB tidak mencukupi. Ada {bnb_balance:.4f} BNB sahaja.")
            await client.close_connection()
            return

        # Binance perlu quantity dengan pembundaran ikut step size, lebih baik round 5 desimal
        quantity_to_sell = float(f"{amount_to_convert:.5f}")

        order = await place_market_order(client, "BNBUSDT", "SELL", quantity_to_sell)

        logging.info(f"[CONVERT] Tukar {quantity_to_sell:.5f} BNB ke USDT (simpan {retain_percent}%)")
        await send_telegram_alert(f"? Tukar {quantity_to_sell:.5f} BNB ke USDT (simpan {retain_percent}%)")

        await client.close_connection()

    except Exception as e:
        logging.exception(f"[CONVERT] Ralat semasa tukar BNB: {e}")
        await send_telegram_alert(f"? Gagal tukar BNB: {e}")

# Contoh run standalone
if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    load_dotenv()

    async def main():
        api_key = os.getenv("BINANCE_API_KEY")
        api_secret = os.getenv("BINANCE_API_SECRET")

        client = await AsyncClient.create(api_key, api_secret)
        symbols = ["BTCUSDT", "ETHUSDT", "BNBUSDT"]
        order_books = await get_order_books_for_symbols(client, symbols)
        for sym, ob in order_books.items():
            print(f"\nOrder book for {sym}:")
            print(ob)
        await convert_max_bnb_to_usdt(retain_percent=40.0)
        await client.close_connection()

    asyncio.run(main())
