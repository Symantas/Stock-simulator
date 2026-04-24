import unittest
from Models.stock import Stock


def _stock(**kw):
    defaults = dict(name="Apple", price=150.0, symbol="APPL",
                    volatility=0.015, sector="Technology")
    defaults.update(kw)
    return Stock(**defaults)


class TestStockCreation(unittest.TestCase):
    def test_valid_stock(self):
        s = _stock()
        self.assertEqual(s.name, "Apple")
        self.assertEqual(s.price, 150.0)
        self.assertEqual(s.symbol, "APPL")
        self.assertEqual(s.volatility, 0.015)
        self.assertEqual(s.sector, "Technology")

    def test_initial_price_in_history(self):
        self.assertEqual(_stock().price_history, [150.0])


class TestStockValidation(unittest.TestCase):
    def test_empty_name_raises(self):
        with self.assertRaises(ValueError):
            _stock(name="")

    def test_negative_price_raises(self):
        with self.assertRaises(ValueError):
            _stock(price=-1.0)

    def test_zero_price_raises(self):
        with self.assertRaises(ValueError):
            _stock(price=0)

    def test_empty_symbol_raises(self):
        with self.assertRaises(ValueError):
            _stock(symbol="")

    def test_volatility_above_one_raises(self):
        with self.assertRaises(ValueError):
            _stock(volatility=1.1)

    def test_negative_volatility_raises(self):
        with self.assertRaises(ValueError):
            _stock(volatility=-0.1)

    def test_empty_sector_raises(self):
        with self.assertRaises(ValueError):
            _stock(sector="")

    def test_bool_price_raises(self):
        with self.assertRaises(ValueError):
            _stock(price=True)


class TestStockPriceHistory(unittest.TestCase):
    def test_record_price_appends(self):
        s = _stock()
        s._record_price(160.0)
        self.assertEqual(s.price_history, [150.0, 160.0])
        self.assertEqual(s.price, 160.0)

    def test_get_value(self):
        self.assertEqual(_stock().get_value(10), 1500.0)


if __name__ == "__main__":
    unittest.main()
