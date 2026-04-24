from Models.asset import Asset
import random

class Market:
    SHOCK_PROBABILITY = 0.01
    SHOCK_MULTIPLIER = 5
    PRICE_FLOOR = 0.01

    def __init__(self, assets):
        if not (isinstance(assets, dict) and len(assets) > 0):
            raise ValueError("Assets must be a non-empty dictionary check the market assets!")
        for symbol, asset in assets.items():
            if not isinstance(asset, Asset):
                raise ValueError(f"The value of the asset with the symbol {symbol} has to be part of asset class check the asset!")
            if symbol != asset.symbol:
                raise ValueError(f"The symbol of the asset has to match they key in the dictionary check the asset!")
        self._assets = assets
        self._tick_count = 0
        self._volatility_multiplier = 1.0

    @property
    def assets(self):
        return self._assets

    def get_asset(self, symbol):
        return self._assets.get(symbol)

    @property
    def tick_count(self):
        return self._tick_count

    @property
    def volatility_multiplier(self):
        return self._volatility_multiplier

    @volatility_multiplier.setter
    def volatility_multiplier(self, value):
        if not (isinstance(value, (int, float)) and not isinstance(value, bool) and value > 0):
            raise ValueError("Volatility multiplier must be a positive number")
        self._volatility_multiplier = value

    def tick(self):
        self._tick_count += 1
        for asset in self._assets.values():
            asset._record_price(self._compute_next_price(asset))

    def _compute_next_price(self, asset):
        if random.random() < self.SHOCK_PROBABILITY:
            bell_width = asset.volatility * self.SHOCK_MULTIPLIER * self._volatility_multiplier
        else:
            bell_width = asset.volatility * self._volatility_multiplier
        # Clamp to -50% floor so no single tick can wipe an asset regardless of mode
        change = max(random.gauss(0, bell_width), -0.5)
        new_price = asset.price * (1 + change)
        return max(new_price, self.PRICE_FLOOR)
