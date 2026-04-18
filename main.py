from Models.factory import load_assets_from_csv
from Models.market import Market
from Models.user import User

assets = load_assets_from_csv("Data/assets.csv")
market = Market(assets)
user = User("Simon", 10000)

print("=" * 60)
print("TEST: Fresh user")
print("=" * 60)
user.display_portfolio()

print()
print("=" * 60)
print("TEST: Buy 10 Apple")
print("=" * 60)
user.buy("APPL", 10, market)
user.display_portfolio()

print()
print("=" * 60)
print("TEST: Sell 3 Apple")
print("=" * 60)
user.sell("APPL", 3, market)
user.display_portfolio()

print()
print("=" * 60)
print("TEST: Market tick — portfolio value changes")
print("=" * 60)
print(f"Before tick: cash=${user.cash:.2f}, portfolio=${user.portfolio.total_value():.2f}")
market.tick()
print(f"After tick:  cash=${user.cash:.2f}, portfolio=${user.portfolio.total_value():.2f}")
user.display_portfolio()

print()
print("=" * 60)
print("TEST: Validators")
print("=" * 60)

try:
    user.buy("FAKE", 10, market)
except ValueError as e:
    print("Caught (fake symbol):", e)

try:
    user.buy("APPL", 99999, market)
except ValueError as e:
    print("Caught (not enough cash):", e)

try:
    user.sell("BTC", 5, market)
except ValueError as e:
    print("Caught (sell unowned):", e)
