from Models.asset import Asset
from Models.validators import is_non_empty_string


class Stock(Asset):
    def __init__(self, name, price, symbol, volatility, sector):
        super().__init__(name, price, symbol, volatility)
        self.sector = sector

    @property
    def sector(self):
        return self._sector

    @sector.setter
    def sector(self, sector):
        if not is_non_empty_string(sector):
            raise ValueError("Sector cannot be empty, and cannot be a non-string value check the stock sector!")
        self._sector = sector

    def display_details(self):
        print(f"{self.name} ({self.symbol}) is in the {self.sector} sector "
              f"with the current price of {self.price} per share")
