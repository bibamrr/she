import urllib.request
import json

url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
req = urllib.request.urlopen(url)
data = json.loads(req.read().decode('utf-8'))
print(f"✅ سعر البيتكوين الحالي من Binance: {data['price']}")
