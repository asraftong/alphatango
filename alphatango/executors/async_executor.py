import logging
from config import Config
from telegram.alerts import send_telegram_message  # Telah ditukar
from arbitrage.pnl_protection import is_pnl_within_threshold
from utils_async import get_order_books_for_symbols
from arbitrage_logic import calculate_triangular_arbitrage
from utils import format_float
from alphaexec.simulation_executor import simulate_trade_and_update_balance

# Import fungsi execute_live_trade hanya jika dalam mod LIVE
if Config.MODE == "LIVE":
    try:
        from executors.live_executor import execute_live_trade
    except ImportError as e:
        logging.error(f"[IMPORT ERROR] Gagal import executors.live_executor: {e}")
        execute_live_trade = None
else:
    execute_live_trade = None

class AsyncExecutor:
    def __init__(self, symbols: list, expected_profit: float, client=None):
        self.symbols = symbols
        self.expected_profit = expected_profit
        self.balance_rm = Config.INITIAL_BALANCE_USDT
        self.balances = {}
        self.client = client

    async def execute_trade(self):
        try:
            logging.info(f"[EXECUTOR] Mula semak peluang arbitrage untuk {self.symbols}")

            # 1. Dapatkan order books
            order_books = await get_order_books_for_symbols(self.symbols, {})

            if not all(symbol in order_books for symbol in self.symbols):
                logging.warning("[EXECUTOR] Tidak semua simbol mempunyai data order book.")
                return

            # 2. Ekstrak harga dari order books
            price_a = float(order_books[self.symbols[0]]['asks'][0][0])
            price_b = float(order_books[self.symbols[1]]['bids'][0][0])
            price_c = float(order_books[self.symbols[2]]['bids'][0][0])

            # 3. Kira keuntungan berpotensi
            profit_rm = calculate_triangular_arbitrage(price_a, price_b, price_c)

            if not is_pnl_within_threshold(profit_rm):
                logging.warning(f"[EXECUTOR] PnL RM{format_float(profit_rm)} melebihi threshold. Trade dibatalkan.")
                return

            logging.info(f"[EXECUTOR] Peluang arbitrage: Untung RM{format_float(profit_rm)}")

            best_opp = {
                'symbol_a': self.symbols[0],
                'symbol_b': self.symbols[1],
                'symbol_c': self.symbols[2],
                'price_a': price_a,
                'price_b': price_b,
                'price_c': price_c,
                'profit_rm': profit_rm
            }

            # ================================
            # === SIMULATION MODE LOGIC ======
            # ================================
            if Config.MODE == "SIMULATION":
                logging.info("[SIMULATION] Menjalankan simulasi dagangan...")

                success, new_balance, profit = await simulate_trade_and_update_balance(
                    best_opp, self.balance_rm, self.balances
                )

                if success:
                    self.balance_rm = new_balance
                    logging.info(f"[SIMULATION] Berjaya. Untung: RM{format_float(profit)}, Baki baru: RM{format_float(new_balance)}")
                else:
                    logging.warning("[SIMULATION] Trade gagal atau tidak menguntungkan.")

            # ===========================
            # === LIVE MODE LOGIC =======
            # ===========================
            elif Config.MODE == "LIVE":
                if execute_live_trade is None:
                    logging.error("[LIVE] Fungsi execute_live_trade tidak tersedia!")
                    await send_telegram_message("?? [ALERT] LIVE mode aktif tetapi executor tidak tersedia!")  # ditukar
                    return

                logging.info("[LIVE] Menjalankan dagangan sebenar...")

                success, executed_price, real_profit = await execute_live_trade(
                    best_opp, self.client
                )

                if success:
                    logging.info(f"[LIVE] Trade berjaya! Harga akhir: {executed_price}, Untung: RM{format_float(real_profit)}")
                else:
                    logging.warning("[LIVE] Trade gagal atau tidak menguntungkan.")

            else:
                logging.warning(f"[EXECUTOR] Mod tidak dikenali: {Config.MODE}")

        except Exception as e:
            logging.error(f"[ERROR] Ralat semasa AsyncExecutor: {e}", exc_info=True)
            await send_telegram_message(f"?? [ALPHATANGO ERROR] AsyncExecutor exception:\n{e}")  # ditukar

# Fungsi tambahan untuk akses baki simulasi (digunakan oleh commands.py)
def get_simulated_balances():
    return AsyncExecutor([], 0).balances
