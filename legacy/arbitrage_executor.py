# arbitrage_executor.py
def detect_arbitrage(prices, threshold_percent=0.2):
    opportunities = []
    symbols = list(prices.keys())

    for i in range(len(symbols)):
        for j in range(i + 1, len(symbols)):
            sym1 = symbols[i]
            sym2 = symbols[j]
            price1 = prices[sym1]
            price2 = prices[sym2]

            diff_percent = abs((price1 - price2) / price1) * 100
            if diff_percent >= threshold_percent:
                opportunities.append({
                    "pair": f"{sym1} ↔ {sym2}",
                    "price1": price1,
                    "price2": price2,
                    "diff_percent": round(diff_percent, 4),
                    "profit_simulated": round(diff_percent / 100 * 10, 5)
                })

    return opportunities
