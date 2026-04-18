class Portfolio():
    def __init__(self):
        self._holdings = {}

    def buy(self, asset, quantity):
        if not (isinstance(quantity, (int, float)) and not isinstance(quantity, bool) and quantity > 0):
            raise ValueError("Quantity must be a positive number check the quantity field!")
        if asset.symbol in self._holdings:
            self._holdings[asset.symbol]["quantity"] += quantity
        else:
            self._holdings[asset.symbol] = {"asset": asset, "quantity": quantity}

    def sell(self, asset, quantity):
        if not (isinstance(quantity, (int, float)) and not isinstance(quantity, bool) and quantity > 0):
            raise ValueError("Quantity must be a positive number check quantity!")
        if not (asset.symbol in self._holdings):
            raise ValueError("You cannot sell an asset you don't own!")
        if not (self._holdings[asset.symbol]["quantity"] >= quantity):
            raise ValueError("You cannot sell more than you own!")
        self._holdings[asset.symbol]["quantity"] -= quantity
        if self._holdings[asset.symbol]["quantity"] == 0:
            del self._holdings[asset.symbol]

    def total_value(self):
        total = 0
        for holding in self._holdings.values():
            total += holding["asset"].price * holding["quantity"]
        return total

    def display_holdings(self):
        if not self._holdings:
            print("Your portfolio is empty!")
        else:
            for holding in self._holdings.values():
                asset = holding["asset"]
                quantity = holding["quantity"]
                price = asset.price
                print(f"{asset.name} ({asset.symbol}): {quantity} units at ${price:.2f} each, total value: ${quantity * price:.2f}")
        
    
                
                 
            
        
    
        