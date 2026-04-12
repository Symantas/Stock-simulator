from Models.stock import Stock
from Models.crypto_asset import CryptoAsset

print("=" * 60)
print("TEST 1: Construct Stock and CryptoAsset after symbol rename")
print("=" * 60)
apple = Stock("Apple", 150, "AAPL", 0.02, "Tech", 0.005)
btc = CryptoAsset("Bitcoin", 60000, "BTC", 0.05, "Bitcoin", 21_000_000, 19_700_000)
apple.display_details()
btc.display_details()
print("apple.symbol:", apple.symbol)
print("btc.symbol:", btc.symbol)
print("apple.price_history:", apple.price_history)
print("btc.price_history:", btc.price_history)

print()
print("=" * 60)
print("TEST 2: _record_price updates price and history atomically")
print("=" * 60)
apple._record_price(153)
apple._record_price(151)
print("apple.price:", apple.price)
print("apple.price_history:", apple.price_history)

print()
print("=" * 60)
print("TEST 3: Polymorphism loop across mixed Asset subclasses")
print("=" * 60)
assets = [
    Stock("Apple", 150, "AAPL", 0.02, "Tech", 0.005),
    CryptoAsset("Bitcoin", 60000, "BTC", 0.05, "Bitcoin", 21_000_000, 19_700_000),
    Stock("Tesla", 250, "TSLA", 0.04, "Auto", 0.0),
    CryptoAsset("Ethereum", 3000, "ETH", 0.06, "Ethereum", 120_000_000, 120_000_000),
]
for asset in assets:
    asset.display_details()
    print()

print("=" * 60)
print("TEST 4: Validators fire on bad input")
print("=" * 60)

try:
    Stock("Tesla", -10, "TSLA", 0.02, "Auto", 0.01)
except ValueError as e:
    print("Caught (negative price):", e)

try:
    apple.dividend_yield = 1.5
except ValueError as e:
    print("Caught (dividend > 1):", e)

try:
    apple.volatility = 2.0
except ValueError as e:
    print("Caught (volatility > 1):", e)

try:
    Stock("", 10, "AAPL", 0.02, "Tech", 0.005)
except ValueError as e:
    print("Caught (empty name):", e)

try:
    Stock("Apple", 150, "", 0.02, "Tech", 0.005)
except ValueError as e:
    print("Caught (empty symbol):", e)

try:
    apple.volatility = True
except ValueError as e:
    print("Caught (bool volatility):", e)

try:
    CryptoAsset("Bad", 60000, "BAD", 0.05, "Bitcoin", 21_000_000, 22_000_000)
except ValueError as e:
    print("Caught (circulation > max):", e)