from abc import ABC, abstractmethod
class Asset(ABC):
    def __init__(self,name,price,symbol,volatility):
        self.name = name
        self.price = price
        self.symbol = symbol
        self.volatility = volatility
        self._price_history = [price]
        
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self,name):
        if isinstance(name,str) and len(name)>0:
            self._name = name
        else:
            raise ValueError("Name must be a non-empty string check the asset name")
        
    @property 
    def price(self):
        return self._price
    @price.setter
    def price(self,price):
        if isinstance(price,(int,float)) and not isinstance(price,bool) and price>0:
            self._price = price
        else:
            raise ValueError("Price must be a positive number check the asset price")
        
        
    @property
    def symbol(self):
        return self._symbol
    @symbol.setter
    def symbol(self,symbol):
        if isinstance(symbol,str) and len(symbol)>0:
            self._symbol = symbol
        else:
            raise ValueError("Symbol must be a non-empty string check the asset symbol")
    @property 
    def volatility(self):
        return self._volatility
    @volatility.setter
    def volatility(self,volatility):
        if isinstance(volatility,(int,float)) and not isinstance(volatility,bool) and 0<= volatility <=1:
            self._volatility = volatility
        else:
            raise ValueError("Volatility must be a number between 0 and 1 check the asset volatility range!")
    @property
    def price_history(self):
        return self._price_history
        
    def get_value(self,quantity):
        return self.price*quantity
    
    
    def _record_price(self,new_price):
        self.price = new_price
        self._price_history.append(new_price)
        
    
    def display(self):
        print(f"{self.name} is worth {self.price}")
     
     
    @abstractmethod
    def display_details(self):
        pass
        
        
