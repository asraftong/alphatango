from config import Config

if Config.MODE == "SIMULATION":
    from executors.async_executor import AsyncExecutor
elif Config.MODE == "LIVE":
    from executors.live_executor import LiveExecutor
else:
    raise ValueError(f"Unknown mode: {Config.MODE}")

def get_executor_instance(symbol: str, base_asset: str, quote_asset: str, expected_profit: float):
    """
    Kembalikan instance executor berdasarkan mode: SIMULATION atau LIVE.

    Args:
        symbol (str): Pasangan simbol.
        base_asset (str): Aset utama.
        quote_asset (str): Aset penukar.
        expected_profit (float): Jangkaan keuntungan.

    Returns:
        Executor instance (AsyncExecutor atau LiveExecutor)
    """
    if Config.MODE == "SIMULATION":
        return AsyncExecutor(symbol, base_asset, quote_asset, expected_profit)
    elif Config.MODE == "LIVE":
        return LiveExecutor(symbol, base_asset, quote_asset, expected_profit)
