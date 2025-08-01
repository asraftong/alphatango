# arbitrage_logic.py

import logging
from config import Config
from utils import format_float

EXCHANGE_RATE_USD_TO_RM = 4.70

def calculate_arbitrage_opportunities(order_books: dict, paths: list, filter_top_n: int = 0) -> list:
    """
    Kira peluang arbitrage segitiga sebenar.

    paths = [
        ('BTCUSDT', 'ETHBTC', 'ETHUSDT'),  # contoh: USDT ? BTC ? ETH ? USDT
    ]
    """
    opportunities = []

    for path in paths:
        try:
            sym1, sym2, sym3 = path
            book1 = order_books.get(sym1)
            book2 = order_books.get(sym2)
            book3 = order_books.get(sym3)

            if not all([book1, book2, book3]):
                continue

            amount_usdt = Config.INITIAL_BALANCE_USDT if Config.MODE == "SIMULATION" else 10.0

            # Langkah 1: USDT ? BASE1 (contoh BTC), beli pada harga ask
            base1_amount = amount_usdt / book1['ask']

            # Langkah 2: BASE1 ? BASE2 (contoh ETH), beli pada harga ask
            base2_amount = base1_amount / book2['ask']

            # Langkah 3: BASE2 ? USDT, jual pada harga bid
            final_usdt = base2_amount * book3['bid']

            profit_usdt = final_usdt - amount_usdt
            profit_rm = profit_usdt * EXCHANGE_RATE_USD_TO_RM

            if profit_rm > 0:
                opportunities.append({
                    "path": f"{sym1} ? {sym2} ? {sym3}",
                    "profit_rm": round(profit_rm, 4),
                    "profit_usdt": round(profit_usdt, 4),
                    "start_amount": format_float(amount_usdt),
                    "end_amount": format_float(final_usdt),
                    "symbols": [sym1, sym2, sym3],
                })

        except Exception as e:
            logging.error(f"[ARBITRAGE LOGIC] Error on path {path}: {e}")
            continue

    if filter_top_n > 0:
        opportunities = sorted(opportunities, key=lambda x: x['profit_rm'], reverse=True)[:filter_top_n]

    return opportunities

# Versi tidak digunakan kini, tapi biar kekal untuk backward compatibility
def calculate_triangular_arbitrage(price_a: float, price_b: float, price_c: float) -> dict:
    profit_percentage = ((price_a * price_b * price_c) - 1.0) * 100
    return {
        "profit_percentage": format_float(profit_percentage, 4),
        "is_profitable": profit_percentage > 0.1
    }
