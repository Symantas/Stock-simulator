import unittest
import tempfile
import os
from Models.factory import load_assets_from_csv
from Models.stock import Stock
from Models.crypto_asset import CryptoAsset

HDR = "type,name,price,symbol,volatility,sector,blockchain,max_supply,circulating_supply\n"


def _write_csv(content):
    f = tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False, encoding="utf-8")
    f.write(HDR + content)
    f.close()
    return f.name


class TestLoadAssetsFromCsv(unittest.TestCase):
    def test_loads_stock(self):
        path = _write_csv("stock,Apple,150.00,APPL,0.015,Technology,,,\n")
        try:
            assets = load_assets_from_csv(path)
            self.assertIn("APPL", assets)
            self.assertIsInstance(assets["APPL"], Stock)
            self.assertEqual(assets["APPL"].price, 150.0)
        finally:
            os.unlink(path)

    def test_loads_crypto(self):
        path = _write_csv("crypto,Bitcoin,30000,BTC,0.04,,Solana,21000000,19000000\n")
        try:
            assets = load_assets_from_csv(path)
            self.assertIn("BTC", assets)
            self.assertIsInstance(assets["BTC"], CryptoAsset)
            self.assertEqual(assets["BTC"].blockchain, "Solana")
        finally:
            os.unlink(path)

    def test_loads_multiple_assets(self):
        path = _write_csv(
            "stock,Apple,150.00,APPL,0.015,Technology,,,\n"
            "stock,Microsoft,250.00,MSFT,0.012,Technology,,,\n"
        )
        try:
            assets = load_assets_from_csv(path)
            self.assertEqual(len(assets), 2)
        finally:
            os.unlink(path)

    def test_unknown_type_raises(self):
        path = _write_csv("bond,Treasury,1000,TBL,0.005,Government,,,\n")
        try:
            with self.assertRaises(ValueError):
                load_assets_from_csv(path)
        finally:
            os.unlink(path)

    def test_symbol_used_as_dict_key(self):
        path = _write_csv("stock,Apple,150.00,APPL,0.015,Technology,,,\n")
        try:
            assets = load_assets_from_csv(path)
            self.assertEqual(list(assets.keys()), ["APPL"])
        finally:
            os.unlink(path)


if __name__ == "__main__":
    unittest.main()
