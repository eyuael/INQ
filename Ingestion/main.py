import asyncio
import json
import websockets
import ssl

BINANCE_WS = "wss://stream.binance.com:9443/ws"

async def depth_stream(symbol: str, levels: int = 10, interval_ms: int = 100):
    stream_name = f"{symbol.lower()}@depth{levels}@{interval_ms}ms"
    url = f"{BINANCE_WS}/{stream_name}"
    
    # Create SSL context that doesn't verify certificates (for testing)
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    
    async with websockets.connect(url, ssl=ssl_context) as ws:
        async for msg in ws:
            yield json.loads(msg)

async def main():
    print("Binance BTCUSDT Order Book Stream")
    print("=" * 40)
    print("Press Ctrl+C to stop\n")
    
    message_count = 0
    try:
        async for data in depth_stream("btcusdt"):
            message_count += 1
            
            print(f"Update #{message_count}:")
            
            if 'bids' in data and data['bids']:
                print("Top 5 Bids:")
                for i, bid in enumerate(data['bids'][:5]):
                    print(f"  {i+1}. Price: ${bid[0]:>10} | Volume: {bid[1]:>12}")
            
            if 'asks' in data and data['asks']:
                print("Top 5 Asks:")
                for i, ask in enumerate(data['asks'][:5]):
                    print(f"  {i+1}. Price: ${ask[0]:>10} | Volume: {ask[1]:>12}")
            
            if data.get('bids') and data.get('asks'):
                best_bid = float(data['bids'][0][0])
                best_ask = float(data['asks'][0][0])
                spread = best_ask - best_bid
                print(f"Spread: ${spread:.2f}")
            
            print("-" * 60)
            
    except KeyboardInterrupt:
        print(f"\nStream stopped. Total updates received: {message_count}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nStopped by user")