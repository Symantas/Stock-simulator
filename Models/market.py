
from Models.asset import Asset


class Market:
    SHOCK_PROBABILITY = 0.01
    SHOCK_MULTIPLIER = 5
    PRICE_FLOOR = 0.01
    
    
    def __init__(self,assets):
        if not (isinstance(assets,dict) and len(assets)>0):
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
        
    def tick(self): 
        self._tick_count +=1
        for asset in self._assets.values():
            new_price = asset.price * 1.01
            asset._record_price(new_price)
            
          
            
        