from Models.stock import Stock
from Models.crypto_asset import CryptoAsset
from Models.market import Market


print("=" * 60)
print("TEST: tick() scaffold with fake +1% formula")
print("=" * 60)

apple = Stock("Apple", 150, "AAPL", 0.02, "Tech", 0.005)
btc = CryptoAsset("Bitcoin", 60000, "BTC", 0.05, "Bitcoin", 21_000_000, 19_700_000)
tesla = Stock("Tesla", 250, "TSLA", 0.04, "Auto", 0.0)

market = Market({"AAPL": apple, "BTC": btc, "TSLA": tesla})

print(f"Initial state (tick {market._tick_count}):")
print(f"  AAPL: {apple.price:.2f}")
print(f"  BTC:  {btc.price:.2f}")
print(f"  TSLA: {tesla.price:.2f}")
print()

print("Running 5 ticks...")
for i in range(5):
    market.tick()
    print(f"  Tick {market._tick_count}: "
          f"AAPL={apple.price:.2f}, "
          f"BTC={btc.price:.2f}, "
          f"TSLA={tesla.price:.2f}")

print()
print("Final price histories (each should have 6 entries: initial + 5 ticks):")
print(f"  AAPL ({len(apple.price_history)} entries): {[round(p, 2) for p in apple.price_history]}")
print(f"  BTC  ({len(btc.price_history)} entries):  {[round(p, 2) for p in btc.price_history]}")
print(f"  TSLA ({len(tesla.price_history)} entries): {[round(p, 2) for p in tesla.price_history]}")

print()
print(f"Final tick count: {market._tick_count}")

print()
print("Sanity check: every price should have grown, none should match starting values")
assert apple.price > 150, "AAPL should have grown"
assert btc.price > 60000, "BTC should have grown"
assert tesla.price > 250, "TSLA should have grown"
assert len(apple.price_history) == 6, "AAPL history should have 6 entries"
assert market._tick_count == 5, "Tick count should be 5"
print("  All assertions passed ✓")