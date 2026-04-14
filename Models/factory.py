import csv
from Models.stock import Stock
from Models.crypto_asset import CryptoAsset


def load_assets_from_csv(path):
    assets = {}
    with open(path, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            asset = _build_asset(row)
            assets[asset.symbol] = asset
    return assets
def _build_asset(row):
    asset_type = row["type"]
    if asset_type == "stock":
        return Stock(row["name"],float(row["price"]),row["symbol"],float(row["volatility"]),row["sector"],float(row["dividend_yield"]))
    elif asset_type == "crypto":
        return CryptoAsset(row["name"],float(row["price"]),row["symbol"],float(row["volatility"]),row["blockchain"],float(row["max_supply"]),float(row["circulating_supply"]))
    else:
        raise ValueError(f"Unknown asset type: {asset_type}!")
    