# /opt/alphatango/alphaexec/simulator.py

import logging
from datetime import datetime
import random
from typing import Tuple, List


class Simulator:
    """
    Simulator untuk menjalankan dagangan arbitrage dalam mod simulasi.
    """
    def __init__(self, initial_balance: float = 1000.0):
        self.balance = initial_balance
        self.trade_log: List[dict] = []

    def execute_trade(self, base_symbol: str, quote_symbol: str, profit: float) -> None:
        """
        Simulasi pelaksanaan dagangan dan kemaskini baki serta log.
        """
        timestamp = datetime.utcnow().isoformat()
        self.balance += profit
        trade = {
            "timestamp": timestamp,
            "pair": f"{base_symbol}/{quote_symbol}",
            "profit": round(profit, 5),
            "balance": round(self.balance, 2),
        }
        self.trade_log.append(trade)
        logging.info(f"?? [SIMULATED ARB] {trade}")

    def get_balance(self) -> float:
        return round(self.balance, 2)

    def get_log(self) -> List[dict]:
        return self.trade_log


# Fungsi ujian simulasi bebas (tidak digunakan dalam loop utama)
async def run_simulation(initial_balance: float) -> None:
    sim = Simulator(initial_balance=initial_balance)
    symbols = ['BTCUSDT', 'ETHUSDT', 'SOLUSDT', 'XRPUSDT']

    for _ in range(3):
        base = random.choice(symbols)
        quote = random.choice(symbols)
        while quote == base:
            quote = random.choice(symbols)

        profit = round(random.uniform(0.01, 5.00), 4)
        sim.execute_trade(base, quote, profit)


# Objekt global simulator untuk digunakan dalam executor SIMULATION
simulator_instance = Simulator(initial_balance=1000)


async def simulate_trade_and_update_balance(opportunity: dict, balance_rm: float, balances: dict) -> Tuple[bool, float, float]:
    """
    Laksanakan dagangan simulasi berdasarkan peluang arbitrage.
    """
    try:
        base = opportunity.get("base", "UNKNOWN")
        quote = opportunity.get("quote", "USDT")
        profit = opportunity.get("profit_rm", 0.0)

        if profit <= 0:
            return False, balance_rm, 0.0

        simulator_instance.execute_trade(base, quote, profit)
        new_balance = simulator_instance.get_balance()
        balances["RM"] = new_balance  # update in-place

        return True, new_balance, profit

    except Exception as e:
        logging.error(f"[SIMULATOR ERROR] {e}")
        return False, balance_rm, 0.0
