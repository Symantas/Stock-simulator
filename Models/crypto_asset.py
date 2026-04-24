from Models.asset import Asset
from Models.validators import is_non_empty_string, is_non_negative_number, is_number_in_range

class CryptoAsset(Asset):
    def __init__(self, name, price, symbol, volatility, blockchain, max_supply, circulating_supply):
        super().__init__(name, price, symbol, volatility)
        self.blockchain = blockchain
        self.max_supply = max_supply
        self.circulating_supply = circulating_supply

    @property
    def blockchain(self):
        return self._blockchain

    @blockchain.setter
    def blockchain(self, blockchain):
        if not is_non_empty_string(blockchain):
            raise ValueError("Blockchain cannot be empty, and cannot be a non-string value check the blockchain field!")
        self._blockchain = blockchain

    @property
    def max_supply(self):
        return self._max_supply

    @max_supply.setter
    def max_supply(self, max_supply):
        if not is_non_negative_number(max_supply):
            raise ValueError("Max supply must be a non-negative number check the max supply field!")
        self._max_supply = max_supply

    @property
    def circulating_supply(self):
        return self._circulating_supply

    @circulating_supply.setter
    def circulating_supply(self, circulating_supply):
        if not is_number_in_range(circulating_supply, 0, self.max_supply):
            raise ValueError("Circulating supply must be between 0 and max supply.")
        self._circulating_supply = circulating_supply

    def display_details(self):
        print(f"{self.name} is a cryptocurrency on the {self.blockchain}  it's symbol is {self.symbol} and the  price is {self.price} per unit with a max supply of {self.max_supply} and a circulating supply of {self.circulating_supply}")
