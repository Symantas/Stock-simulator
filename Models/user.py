from Models.portfolio import Portfolio
from Models.transaction import Transaction
class User:
    def __init__(self,name,cash):
        self.name = name
        self.cash = cash
        self.portfolio = Portfolio()
        self._transactions = Transaction()
        
    @property
    def name(self):
        return self._name
    @name.setter
    def name(self,name):
        if isinstance(name,str) and len(name)>0:
            self._name = name
        else:
            raise ValueError("Name cannot be empty, and cannot be a non-string value check the name field!")
    @property 
    def cash(self):
        return self._cash
    @cash.setter
    def cash(self,cash):
        if isinstance(cash,(int,float)) and not isinstance(cash,bool) and cash>=0:
            self._cash = cash
        else:
            raise ValueError("Cash must be a non-negative number check the cash field!")
        
    def buy(self,symbol,quantity,market):
        asset = market.get_asset(symbol)
        if asset is None:
            raise ValueError("Asset not found in the market check the symbol field!")
        if self._cash < asset.price * quantity:
            raise ValueError("You do not have enough cash to make this purchase check your cash balance!")
        else:
            self._cash -= asset.price * quantity
            self.portfolio.buy(asset,quantity)
            self._transactions.add(asset,quantity,asset.price,"buy",market.tick_count)
    def sell(self,symbol,quantity,market):
        asset=market.get_asset(symbol)
        if asset is None:
            raise ValueError("Asset not found in the market check the symbol field!")
        self.portfolio.sell(asset,quantity)
        self._cash += asset.price * quantity
        self._transactions.add(asset,quantity,asset.price,"sell",market.tick_count)
        
    def display_portfolio(self):
        print(f"{self.name}'s Portfolio:")
        self.portfolio.display_holdings()
        print(f"Cash balance: ${self.cash:.2f}")
        
        print("\nTransaction History:")
        self._transactions.display()
        