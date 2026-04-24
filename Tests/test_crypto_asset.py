import unittest
from Models.crypto_asset import CryptoAsset


def _make_crypto(**kwargs):
    defaults = dict(
        name="Bitcoin", price=30000.0, symbol="BTC",
        volatility=0.04, blockchain="Solana",
        max_supply=21000000.0, circulating_supply=19000000.0,
    )
    defaults.update(kwargs)
    return CryptoAsset(**defaults)


class TestCryptoAssetCreation(unittest.TestCase):
    def test_valid_crypto(self):
        c = _make_crypto()
        self.assertEqual(c.name, "Bitcoin")
        self.assertEqual(c.blockchain, "Solana")
        self.assertEqual(c.max_supply, 21000000.0)
        self.assertEqual(c.circulating_supply, 19000000.0)

    def test_initial_price_in_history(self):
        c = _make_crypto()
        self.assertEqual(c.price_history[0], 30000.0)


class TestCryptoAssetValidation(unittest.TestCase):
    def test_empty_blockchain_raises(self):
        with self.assertRaises(ValueError):
            _make_crypto(blockchain="")

    def test_negative_max_supply_raises(self):
        with self.assertRaises(ValueError):
            _make_crypto(max_supply=-1)

    def test_circulating_exceeds_max_raises(self):
        with self.assertRaises(ValueError):
            _make_crypto(max_supply=1000.0, circulating_supply=2000.0)

    def test_negative_circulating_supply_raises(self):
        with self.assertRaises(ValueError):
            _make_crypto(circulating_supply=-1.0)

    def test_bool_max_supply_raises(self):
        with self.assertRaises(ValueError):
            _make_crypto(max_supply=True)

    def test_negative_price_raises(self):
        with self.assertRaises(ValueError):
            _make_crypto(price=-100.0)


if __name__ == "__main__":
    unittest.main()
