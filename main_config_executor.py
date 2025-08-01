import asyncio
import logging

async def run_simulation_mode():
    logging.info("Running in SIMULATION mode.")
    while True:
        logging.info("Simulated arbitrage scanning...")
        await asyncio.sleep(5)  # gantikan nanti dengan logic AlphaTango sebenar

async def run_live_mode():
    logging.info("Running in LIVE mode.")
    while True:
        logging.info("Live arbitrage scanning...")
        await asyncio.sleep(5)  # gantikan nanti dengan logic AlphaTango sebenar
