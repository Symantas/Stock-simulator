import csv
from Models.stock import Stock
from Models.crypto_asset import CryptoAsset

# Register new asset types here — no changes to _build_asset needed
_ASSET_REGISTRY = {
    "stock": lambda row: Stock(
        row["name"], float(row["price"]), row["symbol"],
        float(row["volatility"]), row["sector"]
    ),
    "crypto": lambda row: CryptoAsset(
        row["name"], float(row["price"]), row["symbol"], float(row["volatility"]),
        row["blockchain"], float(row["max_supply"]), float(row["circulating_supply"])
    ),
}


def load_assets_from_csv(path):
    assets = {}
    with open(path, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            asset = _build_asset(row)
            assets[asset.symbol] = asset
    return assets


def _build_asset(row):
    builder = _ASSET_REGISTRY.get(row["type"])
    if builder is None:
        raise ValueError(f"Unknown asset type: {row['type']}!")
    return builder(row)
