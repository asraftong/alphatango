from binance.client import Client
from config import Config
import logging

def convert_asset_to_usdt(asset: str, percent: float = 100.0):
    try:
        client = Client(Config.BINANCE_API_KEY, Config.BINANCE_API_SECRET)

        symbol = f"{asset}USDT"
        info = client.get_symbol_info(symbol)
        if not info:
            logging.warning(f"[CONVERT] Tiada info untuk {symbol}")
            return False, "Symbol info not found"

        filters = {f['filterType']: f for f in info.get('filters', [])}
        lot_size = float(filters['LOT_SIZE']['stepSize'])
        min_notional = float(filters['MIN_NOTIONAL']['minNotional'])

        balance_info = client.get_asset_balance(asset)
        if not balance_info:
            logging.warning(f"[CONVERT] Tiada baki untuk {asset}")
            return False, "Balance not found"

        total_balance = float(balance_info['free'])
        qty_to_sell = total_balance * (percent / 100)

        # Pembundaran ikut LOT_SIZE
        precision = str(lot_size)[::-1].find('1')
        qty_to_sell = round(qty_to_sell, precision)

        # Dapatkan harga semasa
        price = float(client.get_symbol_ticker(symbol=symbol)['price'])
        notional = price * qty_to_sell

        if notional < min_notional:
            return False, f"Jumlah ({notional:.2f}) bawah min_notional ({min_notional})"

        # Hantar market sell order
        order = client.order_market_sell(
            symbol=symbol,
            quantity=qty_to_sell
        )

        logging.info(f"[CONVERT] Jual {qty_to_sell} {asset} @ {price:.4f} ({notional:.2f} USDT)")
        return True, f"Jual {qty_to_sell} {asset} = {notional:.2f} USDT"

    except Exception as e:
        logging.exception(f"[CONVERT] Ralat convert {asset}: {e}")
        return False, str(e)
