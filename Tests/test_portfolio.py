import unittest
from Models.stock import Stock
from Models.portfolio import Portfolio


def _make_stock(symbol="APPL", price=100.0):
    return Stock("Apple", price, symbol, 0.01, "Technology")


class TestPortfolioBuy(unittest.TestCase):
    def setUp(self):
        self.portfolio = Portfolio()
        self.asset = _make_stock()

    def test_buy_creates_holding(self):
        self.portfolio.buy(self.asset, 10, 100.0)
        self.assertIn("APPL", self.portfolio._holdings)

    def test_buy_sets_quantity(self):
        self.portfolio.buy(self.asset, 10, 100.0)
        self.assertEqual(self.portfolio._holdings["APPL"]["quantity"], 10)

    def test_buy_sets_cost_basis(self):
        self.portfolio.buy(self.asset, 10, 100.0)
        self.assertAlmostEqual(self.portfolio._holdings["APPL"]["cost_basis"], 1000.0)

    def test_buy_accumulates_quantity(self):
        self.portfolio.buy(self.asset, 10, 100.0)
        self.portfolio.buy(self.asset, 5, 120.0)
        self.assertEqual(self.portfolio._holdings["APPL"]["quantity"], 15)

    def test_buy_accumulates_cost_basis(self):
        self.portfolio.buy(self.asset, 10, 100.0)
        self.portfolio.buy(self.asset, 5, 120.0)
        self.assertAlmostEqual(self.portfolio._holdings["APPL"]["cost_basis"], 1600.0)

    def test_buy_invalid_quantity_raises(self):
        with self.assertRaises(ValueError):
            self.portfolio.buy(self.asset, -1, 100.0)

    def test_buy_zero_quantity_raises(self):
        with self.assertRaises(ValueError):
            self.portfolio.buy(self.asset, 0, 100.0)


class TestPortfolioSell(unittest.TestCase):
    def setUp(self):
        self.portfolio = Portfolio()
        self.asset = _make_stock()
        self.portfolio.buy(self.asset, 10, 100.0)

    def test_sell_reduces_quantity(self):
        self.portfolio.sell(self.asset, 4)
        self.assertAlmostEqual(self.portfolio._holdings["APPL"]["quantity"], 6)

    def test_sell_reduces_cost_basis_proportionally(self):
        self.portfolio.sell(self.asset, 5)
        self.assertAlmostEqual(self.portfolio._holdings["APPL"]["cost_basis"], 500.0)

    def test_sell_all_removes_holding(self):
        self.portfolio.sell(self.asset, 10)
        self.assertNotIn("APPL", self.portfolio._holdings)

    def test_sell_more_than_owned_raises(self):
        with self.assertRaises(ValueError):
            self.portfolio.sell(self.asset, 11)

    def test_sell_unowned_asset_raises(self):
        other = _make_stock("MSFT", 200.0)
        with self.assertRaises(ValueError):
            self.portfolio.sell(other, 1)

    def test_sell_fractional_cleans_up(self):
        self.portfolio.buy(self.asset, 0.0000000001, 100.0)
        self.portfolio.sell(self.asset, 10.0000000001)
        self.assertNotIn("APPL", self.portfolio._holdings)


class TestPortfolioPnl(unittest.TestCase):
    def setUp(self):
        self.portfolio = Portfolio()
        self.asset = _make_stock(price=100.0)
        self.portfolio.buy(self.asset, 10, 100.0)

    def test_unrealized_pnl_zero_when_price_unchanged(self):
        self.assertAlmostEqual(self.portfolio.unrealized_pnl(), 0.0)

    def test_unrealized_pnl_positive_on_gain(self):
        self.asset._record_price(120.0)
        self.assertAlmostEqual(self.portfolio.unrealized_pnl(), 200.0)

    def test_unrealized_pnl_negative_on_loss(self):
        self.asset._record_price(80.0)
        self.assertAlmostEqual(self.portfolio.unrealized_pnl(), -200.0)

    def test_unrealized_pnl_by_symbol_keys(self):
        pnl_map = self.portfolio.unrealized_pnl_by_symbol()
        self.assertIn("APPL", pnl_map)

    def test_total_value(self):
        self.assertAlmostEqual(self.portfolio.total_value(), 1000.0)

    def test_total_value_after_price_change(self):
        self.asset._record_price(150.0)
        self.assertAlmostEqual(self.portfolio.total_value(), 1500.0)


if __name__ == "__main__":
    unittest.main()
