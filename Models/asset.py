from abc import ABC, abstractmethod
from Models.validators import is_positive_number, is_non_empty_string, is_number_in_range

class Asset(ABC):
    def __init__(self, name, price, symbol, volatility):
        self.name = name
        self.price = price
        self.symbol = symbol
        self.volatility = volatility
        self._price_history = [price]

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if not is_non_empty_string(name):
            raise ValueError("Name must be a non-empty string check the asset name")
        self._name = name

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, price):
        if not is_positive_number(price):
            raise ValueError("Price must be a positive number check the asset price")
        self._price = price

    @property
    def symbol(self):
        return self._symbol

    @symbol.setter
    def symbol(self, symbol):
        if not is_non_empty_string(symbol):
            raise ValueError("Symbol must be a non-empty string check the asset symbol")
        self._symbol = symbol

    @property
    def volatility(self):
        return self._volatility

    @volatility.setter
    def volatility(self, volatility):
        if not is_number_in_range(volatility, 0, 1):
            raise ValueError("Volatility must be a number between 0 and 1 check the asset volatility range!")
        self._volatility = volatility

    @property
    def price_history(self):
        return self._price_history

    def get_value(self, quantity):
        return self.price * quantity

    def _record_price(self, new_price):
        self.price = new_price
        self._price_history.append(new_price)

    def display(self):
        print(f"{self.name} is worth {self.price}")

    @abstractmethod
    def display_details(self):
        pass
