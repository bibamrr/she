import asyncio
import json
import websockets

async def stream_one_second_klines():
    uri = "wss://stream.binance.com:9443/ws/btcusdt@kline_1s"
    async with websockets.connect(uri) as websocket:
        print("🚀 تم الاتصال بنجاح بـ Binance - يتم استقبال شمعات الثواني الحية للـ BTC:")
        print("-" * 65)
        while True:
            response = await websocket.recv()
            data = json.loads(response)
            k = data['k']
            print(f"الوقت: {k['t']} | السعر الحالي (Close): {k['c']} | الحجم: {k['v']}")

asyncio.run(stream_one_second_klines())
