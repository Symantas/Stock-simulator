from Models.validators import is_positive_number, is_non_negative_int

class Transaction:
    def __init__(self):
        self.history = []

    def add(self, asset, quantity, price, position, tick):
        if position not in ["buy", "sell"]:
            raise ValueError("Position must be either 'buy' or 'sell' check the position field!")
        if not is_positive_number(quantity):
            raise ValueError("Quantity must be a positive number check the quantity field!")
        if not is_positive_number(price):
            raise ValueError("Price must be a positive number check the price field!")
        if not is_non_negative_int(tick):
            raise ValueError("Tick must be a non-negative integer check the tick field!")
        if not hasattr(asset, "symbol") or not hasattr(asset, "name"):
            raise ValueError("Asset must have symbol and name attributes check the asset field!")
        self.history.append({"asset": asset, "quantity": quantity, "price": price, "position": position, "tick": tick})

    def display(self):
        if not self.history:
            print("No transactions yet!")
        else:
            for transaction in self.history:
                asset = transaction["asset"]
                quantity = transaction["quantity"]
                price = transaction["price"]
                position = transaction["position"]
                tick = transaction["tick"]
                print(f"{position.capitalize()} {quantity} units of {asset.name} ({asset.symbol}) at ${price:.2f} each, on tick {tick}.")
