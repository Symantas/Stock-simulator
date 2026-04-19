from Models.factory import load_assets_from_csv
from Models.market import Market
from Models.user import User
import customtkinter as ctk

class StockSimulatorApp:
    def __init__(self):
        self.assets = load_assets_from_csv("Data/assets.csv")
        self.market = Market(self.assets)
        self.user = User("Player1", 50000000)
        self._running = False
        self._selected_asset = None
        self._price_labels = {}

        self.root = ctk.CTk()
        self.root.title("Stock Market Simulator")
        self.root.geometry("1000x650")

        self._build_bottom_bar()
        self.tabs = ctk.CTkTabview(self.root)
        self.tabs.pack(expand=1, fill="both", padx=10, pady=(10, 0))
        self.market_tab = self.tabs.add("Market")
        self.portfolio_tab = self.tabs.add("Portfolio")
        self.transaction_tab = self.tabs.add("Transactions")
        self._build_market_tab()

    def _build_bottom_bar(self):
        bar = ctk.CTkFrame(self.root, height=50, fg_color="#1a1a2e")
        bar.pack(fill="x", side="bottom", padx=10, pady=10)

        self.play_btn = ctk.CTkButton(bar, text="▶ Play", width=80, fg_color="#0f3460", hover_color="#16213e", command=self._play)
        self.play_btn.pack(side="left", padx=10, pady=10)

        self.pause_btn = ctk.CTkButton(bar, text="⏸ Pause", width=80, fg_color="#0f3460", hover_color="#16213e", command=self._pause)
        self.pause_btn.pack(side="left", padx=5, pady=10)

        self.tick_label = ctk.CTkLabel(bar, text="Tick: 0", font=("Arial", 14))
        self.tick_label.pack(side="left", padx=20)

        self.cash_label = ctk.CTkLabel(bar, text=f"Cash: ${self.user.cash:,.2f}", font=("Arial", 14), text_color="#00ff88")
        self.cash_label.pack(side="right", padx=10)

    def _build_market_tab(self):
        left_frame = ctk.CTkFrame(self.market_tab, width=250, fg_color="#1a1a2e")
        left_frame.grid(row=0, column=0, sticky="ns", padx=(10, 5), pady=10)
        left_frame.grid_propagate(False)

        ctk.CTkLabel(left_frame, text="Watchlist", font=("Arial", 20, "bold")).pack(pady=(15, 10))

        for asset in self.market.assets.values():
            row = ctk.CTkFrame(left_frame, fg_color="#16213e", corner_radius=8, cursor="hand2")
            row.pack(fill="x", padx=8, pady=3)

            symbol_label = ctk.CTkLabel(row, text=asset.symbol, font=("Arial", 14, "bold"), anchor="w")
            symbol_label.pack(side="left", padx=(10, 5), pady=8)

            price_label = ctk.CTkLabel(row, text=f"${asset.price:.2f}", font=("Arial", 13), anchor="e", text_color="#00ff88")
            price_label.pack(side="right", padx=(5, 10), pady=8)

            self._price_labels[asset.symbol] = price_label

            row.bind("<Button-1>", lambda e, a=asset: self._select_asset(a))
            symbol_label.bind("<Button-1>", lambda e, a=asset: self._select_asset(a))
            price_label.bind("<Button-1>", lambda e, a=asset: self._select_asset(a))

        self.detail_frame = ctk.CTkFrame(self.market_tab, fg_color="#0f3460")
        self.detail_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 10), pady=10)

        self.detail_label = ctk.CTkLabel(self.detail_frame, text="Select an asset to view details", font=("Arial", 18))
        self.detail_label.pack(expand=True)

        self.market_tab.grid_columnconfigure(1, weight=1)
        self.market_tab.grid_rowconfigure(0, weight=1)

    def _select_asset(self, asset):
        self._selected_asset = asset
        for widget in self.detail_frame.winfo_children():
            widget.destroy()

        ctk.CTkLabel(self.detail_frame, text=asset.name, font=("Arial", 28, "bold")).pack(pady=(20, 5))
        ctk.CTkLabel(self.detail_frame, text=asset.symbol, font=("Arial", 16), text_color="#888888").pack(pady=(0, 15))
        ctk.CTkLabel(self.detail_frame, text=f"${asset.price:,.2f}", font=("Arial", 36, "bold"), text_color="#00ff88").pack(pady=(0, 10))
        ctk.CTkLabel(self.detail_frame, text=f"Volatility: {asset.volatility}", font=("Arial", 14), text_color="#aaaaaa").pack(pady=2)

        if hasattr(asset, "sector"):
            ctk.CTkLabel(self.detail_frame, text=f"Sector: {asset.sector}", font=("Arial", 14), text_color="#aaaaaa").pack(pady=2)
        if hasattr(asset, "blockchain"):
            ctk.CTkLabel(self.detail_frame, text=f"Blockchain: {asset.blockchain}", font=("Arial", 14), text_color="#aaaaaa").pack(pady=2)

    def _play(self):
        self._running = True
        self._tick()

    def _pause(self):
        self._running = False

    def _tick(self):
        self.market.tick()
        self._update_display()
        if self._running:
            self.root.after(1000, self._tick)

    def _update_display(self):
        for symbol, label in self._price_labels.items():
            asset = self.market.get_asset(symbol)
            new_price = asset.price
            label.configure(text=f"${new_price:,.2f}")
        self.tick_label.configure(text=f"Tick: {self.market.tick_count}")
        self.cash_label.configure(text=f"Cash: ${self.user.cash:,.2f}")
        if self._selected_asset:
            self._select_asset(self._selected_asset)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = StockSimulatorApp()
    app.run()
    
