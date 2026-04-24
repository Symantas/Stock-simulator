from Models.validators import is_positive_number


class Portfolio():
    def __init__(self):
        self._holdings = {}

    def buy(self, asset, quantity, price):
        if not is_positive_number(quantity):
            raise ValueError("Quantity must be a positive number check the quantity field!")
        if asset.symbol in self._holdings:
            h = self._holdings[asset.symbol]
            h["cost_basis"] += price * quantity
            h["quantity"] += quantity
        else:
            self._holdings[asset.symbol] = {
                "asset": asset,
                "quantity": quantity,
                "cost_basis": price * quantity,
            }

    def sell(self, asset, quantity):
        if not is_positive_number(quantity):
            raise ValueError("Quantity must be a positive number check quantity!")
        if asset.symbol not in self._holdings:
            raise ValueError("You cannot sell an asset you don't own!")
        h = self._holdings[asset.symbol]
        if h["quantity"] < quantity:
            raise ValueError("You cannot sell more than you own!")
        # Reduce cost basis proportionally
        ratio = quantity / h["quantity"]
        h["cost_basis"] -= h["cost_basis"] * ratio
        h["quantity"] -= quantity
        if h["quantity"] < 1e-9:
            del self._holdings[asset.symbol]

    def unrealized_pnl(self):
        # Market value minus cost basis
        total = 0.0
        for h in self._holdings.values():
            total += h["asset"].price * h["quantity"] - h["cost_basis"]
        return total

    def unrealized_pnl_by_symbol(self):
        # Unrealized P&L per symbol
        return {
            symbol: h["asset"].price * h["quantity"] - h["cost_basis"]
            for symbol, h in self._holdings.items()
        }

    def total_value(self):
        return sum(h["asset"].price * h["quantity"] for h in self._holdings.values())

    def display_holdings(self):
        if not self._holdings:
            print("Your portfolio is empty!")
        else:
            for h in self._holdings.values():
                asset = h["asset"]
                qty = h["quantity"]
                price = asset.price
                print(f"{asset.name} ({asset.symbol}): {qty} units at ${price:.2f} each, "
                      f"total value: ${qty * price:.2f}")
