import logging
import os
import time
from datetime import datetime

start_time = time.time()
last_trade_time = None
trade_counter = 0
latency_log = []

health_log_path = os.path.join("log", "healthcheck.log")

def record_trade():
    global trade_counter, last_trade_time
    trade_counter += 1
    last_trade_time = datetime.now()

def record_latency(ms):
    latency_log.append(ms)
    if len(latency_log) > 100:
        latency_log.pop(0)

def get_uptime():
    elapsed = time.time() - start_time
    hours = int(elapsed // 3600)
    minutes = int((elapsed % 3600) // 60)
    return f"{hours}h {minutes}m"

async def periodic_health_log():
    while True:
        uptime = get_uptime()
        last_trade_str = last_trade_time.strftime("%Y-%m-%d %H:%M:%S") if last_trade_time else "Tiada"
        avg_latency = round(sum(latency_log)/len(latency_log), 2) if latency_log else "-"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        status = (
            f"[{timestamp}] Uptime: {uptime}, "
            f"Jumlah Dagangan: {trade_counter}, "
            f"Trade Terakhir: {last_trade_str}, "
            f"Purata Latency: {avg_latency} ms"
        )

        with open(health_log_path, "a") as f:
            f.write(status + "\n")

        logging.info(f"[HEALTHCHECK] {status}")
        await asyncio.sleep(3600)  # Log setiap 1 jam
