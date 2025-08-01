# /opt/alphatango/alphatango/streamers/price_streamer.py

import asyncio
import json
import websockets
import logging

price_data = {}
LATENCY_THRESHOLD = 1.5  # dalam saat

async def track_latency(uri):
    while True:
        try:
            start = asyncio.get_event_loop().time()
            async with websockets.connect(uri, ping_interval=None) as ws:
                await ws.send(json.dumps({
                    "method": "SUBSCRIBE",
                    "params": ["btcusdt@ticker"],
                    "id": 1
                }))
                await ws.recv()
                end = asyncio.get_event_loop().time()
                latency = round(end - start, 3)
                if latency > LATENCY_THRESHOLD:
                    logging.warning(f"High latency: {latency}s")
                await asyncio.sleep(10)
        except Exception as e:
            logging.error(f"Latency tracking error: {e}")
            await asyncio.sleep(5)

async def start_price_stream(symbols):
    stream_names = [f"{symbol.lower()}@ticker" for symbol in symbols]
    uri = f"wss://stream.binance.com:9443/stream?streams={'/'.join(stream_names)}"

    while True:
        try:
            async with websockets.connect(uri, ping_interval=None) as ws:
                async for message in ws:
                    msg = json.loads(message)
                    data = msg.get("data", {})
                    symbol = data.get("s")
                    bid = float(data.get("b", 0))
                    ask = float(data.get("a", 0))
                    if symbol and bid and ask:
                        price_data[symbol] = {"bid": bid, "ask": ask}
        except Exception as e:
            logging.error(f"WebSocket error: {e}")
            await asyncio.sleep(5)

def get_latest_price(symbol):
    return price_data.get(symbol)
