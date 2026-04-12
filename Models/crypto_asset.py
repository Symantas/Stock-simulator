from Models.asset import Asset
class CryptoAsset(Asset):
    def __init__(self,name,price,symbol,volatility,blockchain,max_supply,circulating_supply):
        super().__init__(name,price,symbol,volatility)
        self.blockchain = blockchain
        self.max_supply = max_supply
        self.circulating_supply = circulating_supply
        
    @property
    def blockchain(self):
        return self._blockchain
    @blockchain.setter
    def blockchain(self,blockchain):
        if isinstance(blockchain,str) and len(blockchain)>0:
            self._blockchain = blockchain
        else:
            raise ValueError("Blockchain cannot be empty, and cannot be a non-string value check the blockchain field!")
    @property
    def max_supply(self):
        return self._max_supply
    @max_supply.setter
    def max_supply(self,max_supply):
        if isinstance(max_supply,(int,float)) and not isinstance(max_supply,bool) and max_supply>=0:
            self._max_supply = max_supply
        else:
            raise ValueError("Max supply must be a non-negative number check the max supply field!")
    @property
    def circulating_supply(self):
        return self._circulating_supply
    @circulating_supply.setter
    def circulating_supply(self,circulating_supply):
        if isinstance(circulating_supply,(int,float)) and not isinstance(circulating_supply,bool) and circulating_supply>=0 and circulating_supply<=self.max_supply:
            self._circulating_supply = circulating_supply
        else:
            raise ValueError("Circulating supply error! must be non negative and cannot exceed max_supply)")
    def display_details(self):
        print(f"{self.name} is a cryptocurrency on the {self.blockchain}  it's symbol is {self.symbol} and the  price is {self.price} per unit with a max supply of {self.max_supply} and a circulating supply of {self.circulating_supply}")
        
        
         