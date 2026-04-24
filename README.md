# Stock Market Simulator

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Body / Analysis](#2-body--analysis)
   - [2.1 OOP Pillars](#21-oop-pillars)
   - [2.2 Design Pattern](#22-design-pattern)
   - [2.3 Composition & Aggregation](#23-composition--aggregation)
   - [2.4 File I/O](#24-file-io)
   - [2.5 Testing](#25-testing)
3. [Results & Summary](#3-results--summary)
4. [Known Limitations](#4-known-limitations)
5. [Resources](#5-resources)

---

## 1. Introduction

### What is this application?

Stock Market Simulator is a desktop application that allows a player to trade virtual stocks and cryptocurrencies against a continuously updating simulated market. Prices evolve each tick using a Gaussian random-walk model — each asset's new price is computed as `new_price = current_price × (1 + ε)`, where ε is drawn from a normal distribution centred on zero with a standard deviation equal to the asset's volatility. Three difficulty modes control how wide that distribution is and how frequently large market shocks occur: **Realistic**, **Volatile**, and **Extremely Volatile**. The player starts with a chosen cash balance and can buy and sell assets freely, tracking their portfolio value and overall profit or loss in real time.

> **Note on AI assistance:** AI was used primarily to help build the GUI layout and to review code for redundancies and logical errors. All business logic, class design, and OOP structure were written by the author.

### How to run the program

**Requirements:** Python 3.10+, `customtkinter`, `matplotlib`

```bash
pip install -r requirements.txt
python main.py
```

On first launch a setup dialog appears — enter a player name and select a starting cash amount (choose a preset or type a custom value), then click **Start Simulation**.

### How to use the program

| Tab | What you can do |
|---|---|
| **Market** | Click any asset in the watchlist to open its detail panel. Enter a quantity and click **Buy** or **Sell**. A price-history chart appears after the first tick. |
| **Portfolio** | View current holdings, per-holding unrealised P&L, and the overall net gain or loss since the session started. Use the **Sell** button on any row for a quick partial sell. |
| **Transactions** | Full history of every buy and sell with price and tick number. |
| **Bottom bar** | ▶ Play / ⏸ Pause the simulation. Switch between **Realistic**, **Volatile**, and **Extremely Volatile** modes. Import additional assets from a CSV file. Click **📄 Report** to save a full session summary to a `.txt` file. |

---

## 2. Body / Analysis

### 2.1 OOP Pillars

#### Encapsulation

Encapsulation means hiding internal state and exposing it only through controlled interfaces. Every model class uses Python `@property` with a validated setter so that no field can be assigned an illegal value from outside the class.

```python
# Models/asset.py
@property
def price(self):
    return self._price

@price.setter
def price(self, price):
    if not is_positive_number(price):
        raise ValueError("Price must be a positive number")
    self._price = price
```

Price is the single most critical piece of state in the simulator — market ticks, portfolio calculations, and P&L figures all depend on it. By routing every write through a validated setter, the program guarantees that no component can accidentally set an asset's price to zero, a negative value, or a non-numeric value. This prevents a whole class of silent bugs that would only surface much later as incorrect portfolio calculations.

---

#### Abstraction

Abstraction means defining *what* something must do without specifying *how*. `Asset` is an abstract base class (ABC) that defines the shared interface for all tradeable assets. It cannot be instantiated directly.

```python
# Models/asset.py
from abc import ABC, abstractmethod

class Asset(ABC):
    def __init__(self, name, price, symbol, volatility):
        ...

    @abstractmethod
    def display_details(self):
        pass
```

The abstract method enforces that every concrete asset subclass must provide its own `display_details` implementation. This matters because `Stock` and `CryptoAsset` have fundamentally different fields — a stock has a sector, while a cryptocurrency has a blockchain, a maximum supply, and a circulating supply. Without the abstract method contract, there would be no guarantee that a new asset subclass correctly implements its own display logic. The rest of the system — `Market`, `Portfolio`, `User` — works against the `Asset` interface without ever needing to know the concrete type it is dealing with.

---

#### Inheritance

`Stock` and `CryptoAsset` both inherit from `Asset`, reusing its shared fields (`name`, `price`, `symbol`, `volatility`, `price_history`) and adding their own.

```python
# Models/stock.py
class Stock(Asset):
    def __init__(self, name, price, symbol, volatility, sector):
        super().__init__(name, price, symbol, volatility)
        self.sector = sector

# Models/crypto_asset.py
class CryptoAsset(Asset):
    def __init__(self, name, price, symbol, volatility,
                 blockchain, max_supply, circulating_supply):
        super().__init__(name, price, symbol, volatility)
        self.blockchain = blockchain
        ...
```

Inheritance eliminates the duplication of the four shared fields and their validated setters, as well as the price history list and `_record_price` logic. Without it, the same validation code would need to be written separately in both `Stock` and `CryptoAsset`. The class hierarchy also models the real-world domain accurately: a stock and a cryptocurrency are both tradeable assets with a price — exactly what the parent class captures — while each subclass adds only what makes it unique.

---

#### Polymorphism

Polymorphism means the same method call behaves differently depending on the object's actual type. `Market.tick()` calls `_record_price()` on every asset without knowing whether it is a `Stock` or a `CryptoAsset`. Similarly, `display_details()` produces different output for each type.

```python
# Models/market.py — works on any Asset subclass
def tick(self):
    self._tick_count += 1
    for asset in self._assets.values():
        asset._record_price(self._compute_next_price(asset))
```

```python
# Stock and CryptoAsset each provide their own version
class Stock(Asset):
    def display_details(self):
        print(f"{self.name} ({self.symbol}) — {self.sector} sector")

class CryptoAsset(Asset):
    def display_details(self):
        print(f"{self.name} on {self.blockchain} blockchain")
```

Polymorphism is valuable here because `Market.tick()` processes every asset in the dictionary with a single loop, regardless of the concrete type. Without it, the loop would require an `if isinstance(asset, Stock) / elif isinstance(asset, CryptoAsset)` chain for every operation, and adding a new asset type would require modifying `Market` directly. With polymorphism, a new asset type only needs to inherit from `Asset` and implement `display_details` — the rest of the system requires no changes.

---

### 2.2 Design Pattern

#### Factory Method

The Factory Method pattern centralises object creation so that the caller does not need to know which concrete class to instantiate. In this project, `_build_asset()` in `Models/factory.py` reads a `type` field from each CSV row and dispatches to the correct constructor via a registry dictionary.

```python
# Models/factory.py
_ASSET_REGISTRY = {
    "stock":  lambda row: Stock(
        row["name"], float(row["price"]), row["symbol"],
        float(row["volatility"]), row["sector"]
    ),
    "crypto": lambda row: CryptoAsset(
        row["name"], float(row["price"]), row["symbol"],
        float(row["volatility"]), row["blockchain"],
        float(row["max_supply"]), float(row["circulating_supply"])
    ),
}

def _build_asset(row):
    builder = _ASSET_REGISTRY.get(row["type"])
    if builder is None:
        raise ValueError(f"Unknown asset type: {row['type']}!")
    return builder(row)
```

The Factory Method is the most suitable pattern here because the application needs to create different asset types from a single flat data source — a CSV file — where the concrete type is only known at runtime. A Singleton would be inappropriate because the goal is flexible object creation, not controlled access to a single global instance. To add a new asset type such as an ETF or a Bond, only one entry needs to be added to `_ASSET_REGISTRY` — the loading logic in `load_assets_from_csv` and everywhere else in the program remains completely unchanged.

---

### 2.3 Composition & Aggregation

#### Composition

Composition is a "has-a" relationship where the child object's lifetime is controlled by the parent. `User` creates its own `Portfolio` and `Transaction` objects — they have no meaning outside of a `User` and are never shared with or passed to any other object.

```python
# Models/user.py
class User:
    def __init__(self, name, cash):
        self.portfolio = Portfolio()        # owned by User
        self._transactions = Transaction()  # owned by User
```

`Portfolio` and `Transaction` are created inside `User.__init__` and are destroyed when the `User` object is discarded. Their entire lifecycle is bound to the user — they cannot exist independently, and no other part of the system creates or holds a reference to them.

---

#### Aggregation

Aggregation is a "has-a" relationship where the child object exists independently of the parent. `Market` holds a dictionary of `Asset` objects that are created outside it and passed in. `Portfolio` stores references to the same assets and does not own them — assets are managed and updated by `Market.tick()`, and `Portfolio` simply reads their current price.

```python
# Models/market.py — assets passed in, not created here
class Market:
    def __init__(self, assets: dict):
        self._assets = assets

# Models/portfolio.py — stores a reference, does not own the asset
self._holdings[asset.symbol] = {
    "asset": asset,   # reference to an Asset owned by Market
    "quantity": quantity,
    "cost_basis": price * quantity,
}
```

Aggregation is the correct relationship between `Portfolio` and `Asset` because assets have an independent identity managed by `Market`. If `Portfolio` owned its own copies of the assets, price updates from `Market.tick()` would not be reflected in portfolio calculations — the portfolio would always show stale prices. By holding a reference to the shared `Asset` object, any price change made by the market is immediately visible in the portfolio.

---

### 2.4 File I/O

#### Reading from file

Assets are loaded from `Data/assets.csv` at startup using Python's `csv.DictReader`. The factory then builds the correct object type for each row.

```python
# Models/factory.py
def load_assets_from_csv(path):
    assets = {}
    with open(path, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            asset = _build_asset(row)
            assets[asset.symbol] = asset
    return assets
```

The same function is reused at runtime when the player clicks **⬆ Import CSV**, allowing new assets to be added to a live session without restarting.

#### Writing to file

Clicking **📄 Report** in the GUI saves a plain-text session report via `filedialog.asksaveasfilename`. The report includes the session summary, every holding with its unrealised P&L, and the full transaction history.

```python
# gui.py — _generate_report()
with open(path, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
```

The report captures the full session state at the moment of saving — cash balance, each holding with its unrealised P&L, and every transaction with its tick number and total value. This gives the player a permanent, human-readable record of any session they wish to preserve, independently of whether the program is running.

---

### 2.5 Testing

Core functionality is covered by **111 unit tests** across 7 files using Python's built-in `unittest` framework.

| File | What is tested |
|---|---|
| `Tests/test_validators.py` | All 5 validation helpers — positive numbers, ranges, strings, ints |
| `Tests/test_stock.py` | Stock creation, all property validators, price history |
| `Tests/test_crypto_asset.py` | CryptoAsset creation, supply constraints |
| `Tests/test_portfolio.py` | Buy/sell logic, cost basis, unrealised P&L, fractional cleanup |
| `Tests/test_transaction.py` | Transaction recording, all 6 validation rules |
| `Tests/test_market.py` | Tick count, price floor, volatility multiplier, asset lookup |
| `Tests/test_user.py` | Cash flow on buy/sell, total P&L, starting cash immutability |
| `Tests/test_factory.py` | CSV loading for stocks and crypto, unknown type error |

Run all tests from the project root:

```bash
python -m unittest discover -s Tests -p "test_*.py" -v
```

The most critical areas to test are the validator helpers and the `Portfolio` buy/sell logic, because every other model class depends on them. If a validator returns an incorrect result, or if the cost-basis arithmetic in `Portfolio` is wrong, errors would propagate silently through P&L calculations and produce incorrect totals that are very difficult to trace.

---

## 3. Results & Summary

### Results

- The price simulation model required several iterations to calibrate. Initial volatility values caused prices to collapse to the floor or grow unrealistically fast within a few ticks. The final per-asset volatility values — stored in the CSV — were chosen to produce believable daily-percentage moves in Realistic mode.
- Separating the GUI display layer from the business logic was the most important structural decision. The market, user, portfolio, and transaction models operate without any dependency on tkinter, which made it straightforward to write unit tests for all model behaviour without needing to mock any GUI components.
- The Factory Method pattern significantly simplified adding the cryptocurrency asset type. Because the registry dispatch was already in place for stocks, adding `CryptoAsset` required only one new entry in `_ASSET_REGISTRY` and the new class itself — nothing else changed.
- Building the validator module early in development paid dividends throughout. Every model setter rejected bad input immediately with a clear error message, which caught several CSV data mistakes during initial testing.
- The tkinter `after()` callback lifecycle required careful handling. Closing the window while the simulation was running caused `invalid command name` errors because pending callbacks fired after their widgets had been destroyed. This was resolved by tracking all scheduled callback IDs and cancelling them in a `WM_DELETE_WINDOW` handler.

### Conclusions

The project successfully implements a real-time stock market simulator demonstrating all four OOP pillars through a clear class hierarchy centred on the abstract `Asset` class. The Factory Method pattern made asset loading extensible without requiring changes to existing code, and keeping the model layer independent of the GUI allowed all business logic to be unit-tested in isolation. Future extensions could include persisting session state between runs, seeding prices from real historical data, or adding a dividend system for stocks.

### How could the application be extended?

- **Session persistence** — serialise the portfolio and transaction history to JSON so a session can be saved and resumed.
- **Real market data seeding** — load historical CSV data from a source such as Yahoo Finance to initialise realistic starting prices and volatility values.
- **Dividend system** — pay periodic cash dividends to holders of stock assets during `Market.tick()`.
- **Multiple portfolios per user** — allow the player to manage separate sub-portfolios with independent P&L tracking.
- **Named market events** — introduce scheduled shocks tied to named events such as earnings reports or central bank decisions to make the simulation more engaging.

---

## 4. Known Limitations

- **No session persistence.** When the program is closed, all price history, portfolio state, and transaction records are lost. The only export option is the plain-text report, which is a one-way snapshot that cannot be loaded back.
- **Simulated prices only.** All asset prices are driven by a Gaussian random-walk model and bear no relation to real market data. The simulator is not suitable for any kind of financial analysis or decision-making.
- **`display_details()` prints to the console only.** The `Asset.display_details()` method implemented by `Stock` and `CryptoAsset` writes to the terminal and has no visible effect in the GUI during normal use.
- **Large-move alerts are console-only.** The "Big move" warning printed by `Market.tick()` appears only in the terminal, not in the GUI status bar, so a player who has not opened a terminal would never see it.
- **Single user, single session.** The application supports exactly one player per run. There is no concept of saving multiple players, comparing sessions, or running multiple simultaneous portfolios.
- **No real-time chart updates.** The price-history chart is drawn once when an asset is selected and is not updated as new ticks arrive. The player must click the asset again to see a refreshed chart.

---

## 5. Resources

- [Python `abc` module — Abstract Base Classes](https://docs.python.org/3/library/abc.html)
- [Python `csv` module](https://docs.python.org/3/library/csv.html)
- [Python `unittest` framework](https://docs.python.org/3/library/unittest.html)
- [CustomTkinter documentation](https://customtkinter.tomschimansky.com/)
- [Matplotlib documentation](https://matplotlib.org/stable/index.html)
- [PEP 8 — Style Guide for Python Code](https://peps.python.org/pep-0008/)
- [Refactoring Guru — Factory Method](https://refactoring.guru/design-patterns/factory-method)
- [Refactoring Guru — Design Patterns](https://refactoring.guru/design-patterns)
