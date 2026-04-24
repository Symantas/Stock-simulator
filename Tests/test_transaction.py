import unittest
from Models.transaction import Transaction
from Models.stock import Stock


def _make_stock():
    return Stock("Apple", 150.0, "APPL", 0.01, "Technology")


class TestTransactionAdd(unittest.TestCase):
    def setUp(self):
        self.tx = Transaction()
        self.asset = _make_stock()

    def test_add_buy_recorded(self):
        self.tx.add(self.asset, 10, 150.0, "buy", 0)
        self.assertEqual(len(self.tx.history), 1)

    def test_add_sell_recorded(self):
        self.tx.add(self.asset, 5, 160.0, "sell", 1)
        self.assertEqual(self.tx.history[0]["position"], "sell")

    def test_record_fields(self):
        self.tx.add(self.asset, 10, 150.0, "buy", 3)
        t = self.tx.history[0]
        self.assertEqual(t["quantity"], 10)
        self.assertEqual(t["price"], 150.0)
        self.assertEqual(t["tick"], 3)
        self.assertIs(t["asset"], self.asset)

    def test_multiple_transactions(self):
        self.tx.add(self.asset, 10, 150.0, "buy", 0)
        self.tx.add(self.asset, 5, 160.0, "sell", 2)
        self.assertEqual(len(self.tx.history), 2)


class TestTransactionValidation(unittest.TestCase):
    def setUp(self):
        self.tx = Transaction()
        self.asset = _make_stock()

    def test_invalid_position_raises(self):
        with self.assertRaises(ValueError):
            self.tx.add(self.asset, 10, 150.0, "hold", 0)

    def test_zero_quantity_raises(self):
        with self.assertRaises(ValueError):
            self.tx.add(self.asset, 0, 150.0, "buy", 0)

    def test_negative_quantity_raises(self):
        with self.assertRaises(ValueError):
            self.tx.add(self.asset, -5, 150.0, "buy", 0)

    def test_zero_price_raises(self):
        with self.assertRaises(ValueError):
            self.tx.add(self.asset, 10, 0, "buy", 0)

    def test_negative_tick_raises(self):
        with self.assertRaises(ValueError):
            self.tx.add(self.asset, 10, 150.0, "buy", -1)

    def test_float_tick_raises(self):
        with self.assertRaises(ValueError):
            self.tx.add(self.asset, 10, 150.0, "buy", 1.5)

    def test_asset_without_symbol_raises(self):
        with self.assertRaises(ValueError):
            self.tx.add(object(), 10, 150.0, "buy", 0)


if __name__ == "__main__":
    unittest.main()
