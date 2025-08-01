import logging
import math
from binance.client import Client

from config import Config
from alphatelegram.alerts import send_telegram_alert
from streamers.price_streamer import price_cache
from scanner.symbol_selector import get_symbol_filters


class LiveExecutor:
    def __init__(self):
        self.client = Client(Config.BINANCE_API_KEY, Config.BINANCE_API_SECRET)
        self.symbol_filters = get_symbol_filters()
        self.last_balance = self.get_usdt_balance()

    def get_usdt_balance(self) -> float:
        """
        Ambil baki semasa USDT daripada akaun Binance.
        """
        try:
            balance_info = self.client.get_asset_balance(asset="USDT")
            return float(balance_info["free"])
        except Exception as e:
            logging.error(f"[BALANCE ERROR] Gagal dapatkan baki USDT: {e}")
            send_telegram_alert(f"?? Gagal dapatkan baki USDT: {e}")
            return 0.0

    def get_min_trade_qty(self, symbol: str) -> float:
        """
        Kira kuantiti minimum berdasarkan harga semasa, minNotional dan LOT_SIZE.
        """
        filters = self.symbol_filters.get(symbol, {})
        lot_size = float(filters.get("LOT_SIZE", {}).get("stepSize", 0.001))
        min_notional = float(filters.get("MIN_NOTIONAL", {}).get("minNotional", 5.0))

        # Ambil harga semasa dari cache
        price = price_cache.get(symbol.upper())
        if price is None:
            raise ValueError(f"Harga semasa untuk {symbol} tidak tersedia dalam cache")

        qty = min_notional / price
        precision = int(round(-math.log10(lot_size)))
        rounded_qty = round(qty // lot_size * lot_size, precision)

        logging.info(
            f"[QTY CALC] {symbol} | Price: {price} | minNotional: {min_notional} | "
            f"LOT_SIZE: {lot_size} | Qty: {rounded_qty}"
        )

        if rounded_qty <= 0:
            raise ValueError(f"Kuantiti dagangan terlalu kecil untuk {symbol}")

        return rounded_qty

    def place_order(self, symbol: str, side: str, quantity: float):
        """
        Hantar order ke Binance menggunakan API Live.
        """
        try:
            order = self.client.create_order(
                symbol=symbol,
                side=side,
                type="MARKET",
                quantity=quantity
            )
            logging.info(f"[ORDER PLACED] {symbol} | {side} | Qty: {quantity}")
            return order
        except Exception as e:
            logging.error(f"[ORDER ERROR] Gagal hantar order: {e}")
            send_telegram_alert(
                f"?? Gagal hantar order {symbol} - {side} - {quantity}\n{e}"
            )
            return None

    def calculate_pnl(self) -> tuple[float, float]:
        """
        Kira PnL berdasarkan perubahan baki USDT.
        """
        current_balance = self.get_usdt_balance()
        pnl = current_balance - self.last_balance
        self.last_balance = current_balance
        return round(pnl, 4), round(current_balance, 2)

    async def execute_trade(self, opportunity: dict):
        """
        Fungsi utama untuk jalankan dagangan berdasarkan peluang arbitrage.
        """
        symbol = opportunity["symbol"]
        side = opportunity["side"]

        try:
            qty = self.get_min_trade_qty(symbol)
            logging.info(f"[EXECUTE] {symbol} | {side} | Kuantiti: {qty}")
            order = self.place_order(symbol, side, qty)

            if order:
                pnl, balance = self.calculate_pnl()
                msg = (
                    f"? LIVE TRADE\n"
                    f"{symbol} | {side}\n"
                    f"Qty: {qty}\n"
                    f"PNL: {pnl:.2f} USDT\n"
                    f"Baki: {balance:.2f} USDT"
                )
                logging.info(f"[PNL] {symbol} | PNL: {pnl:.2f} | Baki: {balance:.2f}")
                send_telegram_alert(msg)

        except Exception as e:
            logging.exception(f"[EXECUTOR ERROR] {e}")
            send_telegram_alert(f"?? Ralat semasa execute_trade:\n{e}")
