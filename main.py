from Models.asset import Asset
from Models.stock import Stock
from Models.crypto_asset import CryptoAsset
from Models.market import Market


print("=" * 60)
print("TEST: get_asset lookup")
print("=" * 60)

apple = Stock("Apple", 150, "AAPL", 0.02, "Tech", 0.005)
btc = CryptoAsset("Bitcoin", 60000, "BTC", 0.05, "Bitcoin", 21_000_000, 19_700_000)
tesla = Stock("Tesla", 250, "TSLA", 0.04, "Auto", 0.0)

market = Market({"AAPL": apple, "BTC": btc, "TSLA": tesla})

# Case 1: existing symbols
found_apple = market.get_asset("AAPL")
print("Found AAPL:", found_apple)
print("  type:", type(found_apple).__name__)
print("  price:", found_apple.price)
print("  name:", found_apple.name)

found_btc = market.get_asset("BTC")
print("Found BTC:", found_btc)
print("  type:", type(found_btc).__name__)
print("  price:", found_btc.price)

# Case 2: missing symbol — should return None, not crash
missing = market.get_asset("DOGE")
print("Missing DOGE:", missing)
print("  is None?", missing is None)

# Case 3: you can still use the returned object normally
apple_from_market = market.get_asset("AAPL")
if apple_from_market is not None:
    apple_from_market.display_details()

print()
print("=" * 60)
print("TEST: Market construction validators still fire")
print("=" * 60)

try:
    Market({})
except ValueError as e:
    print("Caught (empty dict):", e)

try:
    Market([apple, btc])
except ValueError as e:
    print("Caught (not a dict):", e)

try:
    Market({"AAPL": 42})
except ValueError as e:
    print("Caught (value not an Asset):", e)

try:
    Market({"APPL": apple})  # typo in key, apple.symbol is "AAPL"
except ValueError as e:
    print("Caught (key/symbol mismatch):", e)