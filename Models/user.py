from Models.portfolio import Portfolio
from Models.transaction import Transaction
from Models.validators import is_non_empty_string, is_non_negative_number


class User:
    def __init__(self, name, cash):
        self.name = name
        self.cash = cash
        self._starting_cash = cash
        self.portfolio = Portfolio()
        self._transactions = Transaction()

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if not is_non_empty_string(name):
            raise ValueError("Name cannot be empty, and cannot be a non-string value check the name field!")
        self._name = name

    @property
    def cash(self):
        return self._cash

    @cash.setter
    def cash(self, cash):
        if not is_non_negative_number(cash):
            raise ValueError("Cash must be a non-negative number check the cash field!")
        self._cash = cash

    @property
    def starting_cash(self):
        return self._starting_cash

    @property
    def total_pnl(self):
        """Net gain/loss since simulation start."""
        return (self._cash + self.portfolio.total_value()) - self._starting_cash

    def buy(self, symbol, quantity, market):
        asset = market.get_asset(symbol)
        if asset is None:
            raise ValueError("Asset not found in the market check the symbol field!")
        cost = asset.price * quantity
        if self._cash < cost:
            raise ValueError("You do not have enough cash to make this purchase check your cash balance!")
        self._cash -= cost
        self.portfolio.buy(asset, quantity, asset.price)
        self._transactions.add(asset, quantity, asset.price, "buy", market.tick_count)

    def sell(self, symbol, quantity, market):
        asset = market.get_asset(symbol)
        if asset is None:
            raise ValueError("Asset not found in the market check the symbol field!")
        self.portfolio.sell(asset, quantity)
        self._cash += asset.price * quantity
        self._transactions.add(asset, quantity, asset.price, "sell", market.tick_count)

    def display_portfolio(self):
        print(f"{self.name}'s Portfolio:")
        self.portfolio.display_holdings()
        print(f"Cash balance: ${self.cash:.2f}")
        print(f"Total P&L: ${self.total_pnl:+,.2f}")
        print("\nTransaction History:")
        self._transactions.display()
