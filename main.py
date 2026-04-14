from Models.factory import load_assets_from_csv
from Models.market import Market

assets = load_assets_from_csv("Data/assets.csv")
market = Market(assets)

print(f"Loaded market with {len(market.assets)} assets from CSV")
print()

for i in range(15):
    market.tick()
    prices = "  ".join(
        f"{a.symbol}={a.price:.2f}" for a in market.assets.values()
    )
    print(f"Tick {market._tick_count:2d}: {prices}")
