import asyncio
import json
import websockets

BINANCE_WS = "wss://data-stream.binance.vision/ws"

async def depth_stream(symbol: str, levels: int = 10, interval_ms: int = 100):
    stream_name = f"{symbol.lower()}@depth{levels}@{interval_ms}ms"
    url = f"{BINANCE_WS}/{stream_name}"

    async for ws in websockets.connect(url, ping_interval=15):
        try:
            async for msg in ws:
                yield json.loads(msg)
        except websockets.ConnectionClosed:
            continue

depth_stream("btcusdt")