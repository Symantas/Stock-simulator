class Transaction:
    def __init__(self):
        self.history = []

    def add(self, asset, quantity, price, position, tick):
        if position not in ["buy", "sell"]:
            raise ValueError("Position must be either 'buy' or 'sell' check the position field!")
        if not (isinstance(quantity, (int, float)) and not isinstance(quantity, bool) and quantity > 0):
            raise ValueError("Quantity must be a positive number check the quantity field!")
        if not (isinstance(price, (int, float)) and not isinstance(price, bool) and price > 0):
            raise ValueError("Price must be a positive number check the price field!")
        if not (isinstance(tick, int) and tick >= 0):
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