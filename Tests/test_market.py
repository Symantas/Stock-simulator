import unittest
from Models.market import Market
from Models.stock import Stock


def _make_market():
    assets = {
        "APPL": Stock("Apple", 150.0, "APPL", 0.01, "Technology"),
        "MSFT": Stock("Microsoft", 250.0, "MSFT", 0.01, "Technology"),
    }
    return Market(assets)


class TestMarketInit(unittest.TestCase):
    def test_empty_dict_raises(self):
        with self.assertRaises(ValueError):
            Market({})

    def test_non_asset_value_raises(self):
        with self.assertRaises(ValueError):
            Market({"APPL": "not an asset"})

    def test_mismatched_symbol_raises(self):
        asset = Stock("Apple", 150.0, "APPL", 0.01, "Technology")
        with self.assertRaises(ValueError):
            Market({"WRONG": asset})

    def test_initial_tick_count(self):
        m = _make_market()
        self.assertEqual(m.tick_count, 0)


class TestMarketTick(unittest.TestCase):
    def test_tick_increments_count(self):
        m = _make_market()
        m.tick()
        self.assertEqual(m.tick_count, 1)

    def test_tick_changes_prices(self):
        # Run many ticks — statistically prices will differ from start
        m = _make_market()
        original = {s: a.price for s, a in m.assets.items()}
        for _ in range(50):
            m.tick()
        changed = any(m.assets[s].price != original[s] for s in original)
        self.assertTrue(changed)

    def test_price_history_grows(self):
        m = _make_market()
        m.tick()
        m.tick()
        self.assertEqual(len(m.assets["APPL"].price_history), 3)

    def test_price_never_goes_below_floor(self):
        m = _make_market()
        for _ in range(200):
            m.tick()
        for asset in m.assets.values():
            self.assertGreaterEqual(asset.price, Market.PRICE_FLOOR)


class TestMarketGetAsset(unittest.TestCase):
    def test_get_existing_asset(self):
        m = _make_market()
        self.assertIsNotNone(m.get_asset("APPL"))

    def test_get_unknown_returns_none(self):
        m = _make_market()
        self.assertIsNone(m.get_asset("UNKNOWN"))


class TestMarketVolatilityMultiplier(unittest.TestCase):
    def test_default_multiplier(self):
        m = _make_market()
        self.assertEqual(m.volatility_multiplier, 1.0)

    def test_set_valid_multiplier(self):
        m = _make_market()
        m.volatility_multiplier = 2.5
        self.assertEqual(m.volatility_multiplier, 2.5)

    def test_zero_multiplier_raises(self):
        m = _make_market()
        with self.assertRaises(ValueError):
            m.volatility_multiplier = 0

    def test_negative_multiplier_raises(self):
        m = _make_market()
        with self.assertRaises(ValueError):
            m.volatility_multiplier = -1.0


if __name__ == "__main__":
    unittest.main()
