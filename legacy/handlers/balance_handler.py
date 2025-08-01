from config import Config
from simulator import Simulator
from executors.live_executor import LiveExecutor

def get_current_balance():
    """
    Dapatkan baki semasa berdasarkan mode (SIMULATION atau LIVE)
    """
    if Config.MODE == "SIMULATION":
        return Simulator.get_balance(Config.QUOTE_CURRENCY)
    elif Config.MODE == "LIVE":
        executor = LiveExecutor()
        return executor.get_live_balance(Config.QUOTE_CURRENCY)
    else:
        raise ValueError(f"Mode tidak sah: {Config.MODE}")
