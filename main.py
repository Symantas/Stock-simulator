from Models.stock import Stock
from Models.crypto_asset import CryptoAsset
from Models.market import Market

# Temporarily crank shock probability so we actually see dramatic moves
Market.SHOCK_PROBABILITY = 0.3

apple = Stock("Apple", 150, "AAPL", 0.02, "Tech", 0.005)
btc = CryptoAsset("Bitcoin", 60000, "BTC", 0.05, "Bitcoin", 21_000_000, 19_700_000)
tesla = Stock("Tesla", 250, "TSLA", 0.04, "Auto", 0.0)

market = Market({"AAPL": apple, "BTC": btc, "TSLA": tesla})

print("Running 20 ticks with cranked shock probability (0.3)...")
print()

for i in range(20):
    market.tick()
    print(f"Tick {market._tick_count:2d}: "
          f"AAPL={apple.price:8.2f}  "
          f"BTC={btc.price:10.2f}  "
          f"TSLA={tesla.price:8.2f}")