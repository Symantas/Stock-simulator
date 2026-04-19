from Models.factory import load_assets_from_csv
from Models.market import Market
from Models.user import User

assets = load_assets_from_csv("Data/assets.csv")
market = Market(assets)
user = User("Simon", 50000000)

print("=" * 60)
print("TEST: Buy and sell with transaction recording")
print("=" * 60)

user.buy("APPL", 10, market)
user.buy("BTC", 1, market)
print("After buying 10 APPL and 1 BTC:")
user.display_portfolio()

print()
market.tick()
market.tick()
market.tick()
print("After 3 market ticks:")
user.display_portfolio()

print()
user.sell("APPL", 5, market)
print("After selling 5 APPL:")
user.display_portfolio()