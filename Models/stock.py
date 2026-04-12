from Models.asset import Asset
class Stock(Asset):
    def __init__(self,name,price,symbol,volatility,sector,dividend_yield):
        super().__init__(name,price,symbol,volatility)
        self.sector = sector
        self.dividend_yield = dividend_yield
        
        
    
    @property
    def sector(self):
        return self._sector
    @sector.setter
    def sector(self,sector):
        if isinstance(sector,str) and len(sector)>0:
            self._sector = sector
        else:
            raise ValueError("Sector cannot be empty, and cannot be a non-string value check the stock sector!")
    @property
    def dividend_yield(self):
        return self._dividend_yield
    @dividend_yield.setter
    def dividend_yield(self,dividend_yield):
        if isinstance(dividend_yield,(int,float)) and not isinstance(dividend_yield,bool) and 0<= dividend_yield <=1:
            self._dividend_yield = dividend_yield
        else:
            raise ValueError("Dividend yield must be a number between 0 and 1 check the stock dividend yield range!")
        
    def display_details(self):
        print(f"{self.name} ({self.symbol}) is in the {self.sector} sector with the current price of {self.price} per share and a dividend of {self.dividend_yield*100}%")
        