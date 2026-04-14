#Stock Simulator - TODO
##TODO:
# Stock Simulator — TODO

## To do before deadline
- [ ] Implement dividend payout in Market.tick() once Portfolio exists
- [ ] Factory + CSV loading (in progress)
- [ ] Portfolio class (composition/aggregation)
- [ ] User class (cash, buy/sell logic)
- [ ] Transaction record class
- [ ] Unit tests with unittest framework
- [ ] Write README.md report (intro, body, results, conclusions)

## Polish-pass ideas (if time permits)
- [ ] Add __str__ methods to Asset subclasses for cleaner debug printing
- [ ] Tighten symbol validator to enforce uppercase alphanumeric, 1-6 chars
- [ ] Run `black` on all Python files for PEP8 cleanup
- [ ] Thousands separators in display_details (f"{value:,}")

## Future extensions (for "how to extend" report section)
- [ ] Calibrate volatility from real historical data (Yahoo/CoinGecko CSV)
- [ ] Implement calculate_historical_volatility() method on Asset
- [ ] Delist assets that crash below floor (more realistic than clipping)
- [ ] Support multiple portfolios per user
- [ ] Add random.seed(42) option for reproducible tests
- [ ] Event system with named events (earnings, hacks, Fed decisions)