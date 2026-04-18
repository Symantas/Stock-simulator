from Models.factory import load_assets_from_csv
from Models.market import Market
from Models.portfolio import Portfolio

assets = load_assets_from_csv("Data/assets.csv")
market = Market(assets)
portfolio = Portfolio()

apple = market.get_asset("APPL")
btc = market.get_asset("BTC")

print("=" * 60)
print("TEST: Empty portfolio")
print("=" * 60)
portfolio.display_holdings()

print()
print("=" * 60)
print("TEST: Buy 10 Apple and 2 Bitcoin")
print("=" * 60)
portfolio.buy(apple, 10)
portfolio.buy(btc, 2)
portfolio.display_holdings()
print(f"Total value: ${portfolio.total_value():.2f}")

print()
print("=" * 60)
print("TEST: Buy 5 more Apple (should increase to 15)")
print("=" * 60)
portfolio.buy(apple, 5)
portfolio.display_holdings()
print(f"Total value: ${portfolio.total_value():.2f}")

print()
print("=" * 60)
print("TEST: Sell 3 Apple")
print("=" * 60)
portfolio.sell(apple, 3)
portfolio.display_holdings()
print(f"Total value: ${portfolio.total_value():.2f}")

print()
print("=" * 60)
print("TEST: Market tick — prices change, portfolio value follows")
print("=" * 60)
print(f"Before tick: APPL=${apple.price:.2f}, BTC=${btc.price:.2f}")
print(f"Before tick: Total value: ${portfolio.total_value():.2f}")
market.tick()
print(f"After tick:  APPL=${apple.price:.2f}, BTC=${btc.price:.2f}")
print(f"After tick:  Total value: ${portfolio.total_value():.2f}")

print()
print("=" * 60)
print("TEST: Sell all remaining Apple")
print("=" * 60)
portfolio.sell(apple, 12)
portfolio.display_holdings()

print()
print("=" * 60)
print("TEST: Validators")
print("=" * 60)

try:
    portfolio.sell(apple, 5)
except ValueError as e:
    print("Caught (sell asset not owned):", e)

try:
    portfolio.buy(apple, -10)
except ValueError as e:
    print("Caught (negative quantity):", e)

try:
    portfolio.sell(btc, 999)
except ValueError as e:
    print("Caught (sell more than owned):", e)
