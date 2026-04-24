
from Models.asset import Asset
import random
from Models.validators import is_positive_integer
class Market:
    SHOCK_PROBABILITY = 0.01
    SHOCK_MULTIPLIER = 5
    PRICE_FLOOR = 0.01
    
    
    def __init__(self,assets):
        if not (isinstance(assets,dict) and is_positive_integer(len(assets))):
            raise ValueError("Assets must be a non-empty dictionary check the market assets!")

        for symbol, asset in assets.items():
            if not isinstance(asset,Asset):
                raise ValueError(f"The value of the asset with the symbol {symbol} has to be part of asset class check the asset!")
            if symbol != asset.symbol:
                raise ValueError(f"The symbol of the asset has to match they key  in the dictionary check the asset!")
            
        self._assets = assets
        self._tick_count = 0
    @property
    def assets(self):
        return self._assets
    
    def get_asset(self,symbol):
            return self._assets.get(symbol)
        
    @property
    def tick_count(self):
        return self._tick_count
    
    
    def tick(self): 
        self._tick_count +=1
        for asset in self._assets.values():
            old_price = asset.price
            new_price = self._compute_next_price(asset)
            if abs((new_price - old_price) / old_price) > (asset.volatility * 3):
                print(f"** Big move on {asset.symbol}!, trade with caution! **")
            asset._record_price(new_price)
            
          
    def _compute_next_price(self,asset):
      if  random.random() < self.SHOCK_PROBABILITY:
          bell_width = asset.volatility * self.SHOCK_MULTIPLIER
      else:
          bell_width = asset.volatility
      change = random.gauss(0,bell_width)
      new_price = asset.price * (1 + change)
      new_price = max(new_price,self.PRICE_FLOOR)
      return new_price
        
        