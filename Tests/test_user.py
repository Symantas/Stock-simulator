import unittest
from Models.market import Market
from Models.stock import Stock
from Models.user import User


def _make_market():
    assets = {"APPL": Stock("Apple", 100.0, "APPL", 0.01, "Technology")}
    return Market(assets)


class TestUserInit(unittest.TestCase):
    def test_name_and_cash(self):
        u = User("Alice", 1000.0)
        self.assertEqual(u.name, "Alice")
        self.assertEqual(u.cash, 1000.0)

    def test_starting_cash_fixed(self):
        u = User("Alice", 1000.0)
        self.assertEqual(u.starting_cash, 1000.0)

    def test_initial_pnl_is_zero(self):
        u = User("Alice", 1000.0)
        self.assertEqual(u.total_pnl, 0.0)

    def test_empty_name_raises(self):
        with self.assertRaises(ValueError):
            User("", 1000.0)

    def test_negative_cash_raises(self):
        with self.assertRaises(ValueError):
            User("Alice", -1.0)


class TestUserBuy(unittest.TestCase):
    def setUp(self):
        self.market = _make_market()
        self.user = User("Alice", 10000.0)

    def test_buy_deducts_cash(self):
        self.user.buy("APPL", 10, self.market)
        self.assertAlmostEqual(self.user.cash, 9000.0)

    def test_buy_adds_to_portfolio(self):
        self.user.buy("APPL", 10, self.market)
        self.assertIn("APPL", self.user.portfolio._holdings)

    def test_buy_unknown_symbol_raises(self):
        with self.assertRaises(ValueError):
            self.user.buy("UNKNOWN", 1, self.market)

    def test_buy_insufficient_cash_raises(self):
        with self.assertRaises(ValueError):
            self.user.buy("APPL", 200, self.market)

    def test_buy_recorded_in_transactions(self):
        self.user.buy("APPL", 5, self.market)
        self.assertEqual(len(self.user._transactions.history), 1)
        self.assertEqual(self.user._transactions.history[0]["position"], "buy")


class TestUserSell(unittest.TestCase):
    def setUp(self):
        self.market = _make_market()
        self.user = User("Alice", 10000.0)
        self.user.buy("APPL", 10, self.market)

    def test_sell_returns_cash(self):
        self.user.sell("APPL", 5, self.market)
        self.assertAlmostEqual(self.user.cash, 9500.0)

    def test_sell_removes_from_portfolio(self):
        self.user.sell("APPL", 10, self.market)
        self.assertNotIn("APPL", self.user.portfolio._holdings)

    def test_sell_more_than_owned_raises(self):
        with self.assertRaises(ValueError):
            self.user.sell("APPL", 11, self.market)

    def test_sell_recorded_in_transactions(self):
        self.user.sell("APPL", 5, self.market)
        positions = [t["position"] for t in self.user._transactions.history]
        self.assertIn("sell", positions)


class TestUserTotalPnl(unittest.TestCase):
    def setUp(self):
        self.market = _make_market()
        self.user = User("Alice", 1000.0)

    def test_pnl_positive_after_price_rise(self):
        self.user.buy("APPL", 5, self.market)
        self.market.assets["APPL"]._record_price(200.0)
        self.assertGreater(self.user.total_pnl, 0)

    def test_pnl_negative_after_price_drop(self):
        self.user.buy("APPL", 5, self.market)
        self.market.assets["APPL"]._record_price(50.0)
        self.assertLess(self.user.total_pnl, 0)

    def test_starting_cash_unchanged_by_trades(self):
        self.user.buy("APPL", 5, self.market)
        self.user.sell("APPL", 5, self.market)
        self.assertEqual(self.user.starting_cash, 1000.0)


if __name__ == "__main__":
    unittest.main()
