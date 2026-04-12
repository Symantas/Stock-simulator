from Models.asset import Asset
class Stock(Asset):
    def __init__(self,name,price,ticker,sector):
        super().__init__(name,price)
        self.ticker = ticker
        self.sector = sector
        
        
    @property
    def ticker(self):
        return self._ticker
    @ticker.setter
    def ticker(self,ticker):
        if isinstance(ticker,str) and len(ticker)>0:
            self._ticker = ticker
        else:
            raise ValueError("Ticker cannot be empty, and cannot be a non-string value check the stock ticker!")
    @property
    def sector(self):
        return self._sector
    @sector.setter
    def sector(self,sector):
        if isinstance(sector,str) and len(sector)>0:
            self._sector = sector
        else:
            raise ValueError("Sector cannot be empty, and cannot be a non-string value check the stock sector!")
    