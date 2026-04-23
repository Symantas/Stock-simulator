from Models.factory import load_assets_from_csv
from Models.market import Market
from Models.user import User
import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

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
        self._build_portfolio_tab()
        self._build_transaction_tab()
        self._update_portfolio_display()
        self._update_transaction_display()

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

        buy_sell_frame = ctk.CTkFrame(self.detail_frame, fg_color="transparent")
        buy_sell_frame.pack(pady=20)

        self.qty_entry = ctk.CTkEntry(buy_sell_frame, placeholder_text="Quantity", width=120)
        self.qty_entry.pack(side="left", padx=5)

        ctk.CTkButton(buy_sell_frame, text="Buy", width=80, fg_color="#00aa55", hover_color="#008844", command=self._handle_buy).pack(side="left", padx=5)
        ctk.CTkButton(buy_sell_frame, text="Sell", width=80, fg_color="#cc3333", hover_color="#aa2222", command=self._handle_sell).pack(side="left", padx=5)

        if len(asset.price_history) > 1:
            fig, ax = plt.subplots(figsize=(5, 2.5))
            fig.patch.set_facecolor("#0f3460")
            ax.set_facecolor("#1a1a2e")
            ax.plot(asset.price_history, color="#00ff88", linewidth=1.5)
            ax.tick_params(colors="#aaaaaa", labelsize=8)
            ax.spines[:].set_color("#333355")
            ax.set_xlabel("Tick", color="#aaaaaa", fontsize=8)
            ax.set_ylabel("Price", color="#aaaaaa", fontsize=8)
            fig.tight_layout(pad=1.0)
            canvas = FigureCanvasTkAgg(fig, master=self.detail_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="x", padx=15, pady=(5, 15))
            plt.close(fig)

    def _build_portfolio_tab(self):
        self.portfolio_frame = ctk.CTkFrame(self.portfolio_tab, fg_color="#0f3460")
        self.portfolio_frame.pack(fill="both", expand=True, padx=10, pady=10)

    def _build_transaction_tab(self):
        self.transaction_frame = ctk.CTkFrame(self.transaction_tab, fg_color="#0f3460")
        self.transaction_frame.pack(fill="both", expand=True, padx=10, pady=10)

    def _update_portfolio_display(self):
        for widget in self.portfolio_frame.winfo_children():
            widget.destroy()

        ctk.CTkLabel(self.portfolio_frame, text="Portfolio", font=("Arial", 28, "bold")).pack(pady=(20, 15))

        portfolio_value = self.user.portfolio.total_value()
        total_value = self.user.cash + portfolio_value

        info_frame = ctk.CTkFrame(self.portfolio_frame, fg_color="#1a1a2e", corner_radius=8)
        info_frame.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(info_frame, text=f"Cash: ${self.user.cash:,.2f}", font=("Arial", 16), text_color="#00ff88").pack(anchor="w", padx=15, pady=10)
        ctk.CTkLabel(info_frame, text=f"Holdings Value: ${portfolio_value:,.2f}", font=("Arial", 16), text_color="#00ffff").pack(anchor="w", padx=15, pady=5)
        ctk.CTkLabel(info_frame, text=f"Total Value: ${total_value:,.2f}", font=("Arial", 18, "bold"), text_color="#ffff00").pack(anchor="w", padx=15, pady=10)

        if self.user.portfolio._holdings:
            holdings_label = ctk.CTkLabel(self.portfolio_frame, text="Holdings", font=("Arial", 20, "bold"))
            holdings_label.pack(pady=(20, 10), anchor="w", padx=20)

            holdings_scroll = ctk.CTkScrollableFrame(self.portfolio_frame, fg_color="#1a1a2e")
            holdings_scroll.pack(fill="both", expand=True, padx=20, pady=10)

            for symbol, holding in self.user.portfolio._holdings.items():
                asset = holding["asset"]
                qty = holding["quantity"]
                value = asset.price * qty

                qty_str = f"{qty:.2f}".rstrip('0').rstrip('.') if qty % 1 != 0 else f"{int(qty)}"

                row = ctk.CTkFrame(holdings_scroll, fg_color="#16213e", corner_radius=8)
                row.pack(fill="x", pady=5)

                ctk.CTkLabel(row, text=asset.name, font=("Arial", 14, "bold"), anchor="w").pack(side="left", padx=10, pady=8, expand=True, fill="x")
                ctk.CTkLabel(row, text=f"{qty_str} units", font=("Arial", 12), text_color="#aaaaaa", anchor="center").pack(side="left", padx=5, pady=8)
                ctk.CTkLabel(row, text=f"@ ${asset.price:,.2f}", font=("Arial", 12), text_color="#00ff88", anchor="center").pack(side="left", padx=5, pady=8)
                ctk.CTkLabel(row, text=f"${value:,.2f}", font=("Arial", 13, "bold"), text_color="#00ffff", anchor="center").pack(side="left", padx=5, pady=8)
                ctk.CTkButton(row, text="Sell", width=60, fg_color="#cc3333", hover_color="#aa2222", command=lambda s=symbol, q=qty: self._quick_sell(s, q)).pack(side="right", padx=10, pady=8)
        else:
            ctk.CTkLabel(self.portfolio_frame, text="Portfolio is empty", font=("Arial", 16), text_color="#888888").pack(pady=40)

    def _update_transaction_display(self):
        for widget in self.transaction_frame.winfo_children():
            widget.destroy()

        ctk.CTkLabel(self.transaction_frame, text="Transaction History", font=("Arial", 28, "bold")).pack(pady=(20, 15))

        if self.user._transactions.history:
            trans_scroll = ctk.CTkScrollableFrame(self.transaction_frame, fg_color="#1a1a2e")
            trans_scroll.pack(fill="both", expand=True, padx=20, pady=10)

            for i, trans in enumerate(self.user._transactions.history):
                asset = trans["asset"]
                qty = trans["quantity"]
                price = trans["price"]
                position = trans["position"]
                tick = trans["tick"]
                total = qty * price

                qty_str = f"{qty:.2f}".rstrip('0').rstrip('.') if qty % 1 != 0 else f"{int(qty)}"

                color = "#00ff88" if position == "buy" else "#ff6666"
                bg_color = "#0d2818" if position == "buy" else "#330000"

                row = ctk.CTkFrame(trans_scroll, fg_color=bg_color, corner_radius=8)
                row.pack(fill="x", pady=5)

                action_text = f"{'BUY' if position == 'buy' else 'SELL'} {qty_str}x {asset.symbol}"
                ctk.CTkLabel(row, text=action_text, font=("Arial", 13, "bold"), text_color=color, anchor="w").pack(side="left", padx=10, pady=8, expand=True, fill="x")

                details_text = f"@ ${price:,.2f} • Tick {tick}"
                ctk.CTkLabel(row, text=details_text, font=("Arial", 12), text_color="#aaaaaa", anchor="center").pack(side="left", padx=5, pady=8)

                ctk.CTkLabel(row, text=f"${total:,.2f}", font=("Arial", 12, "bold"), text_color=color, anchor="e").pack(side="right", padx=10, pady=8)
        else:
            ctk.CTkLabel(self.transaction_frame, text="No transactions yet", font=("Arial", 16), text_color="#888888").pack(pady=40)

    def _quick_sell(self, symbol, available_qty):
        dialog = ctk.CTkInputDialog(text=f"Enter quantity to sell (max: {available_qty:.2f}):", title="Sell")
        qty_str = dialog.get_input()

        if qty_str is None or qty_str == "":
            return

        try:
            qty = float(qty_str)
            if qty <= 0:
                print("Quantity must be positive")
                return
            if qty > available_qty:
                print(f"Cannot sell more than {available_qty:.2f} units")
                return
            self.user.sell(symbol, qty, self.market)
            self._update_display()
            print(f"Sold {qty} {symbol}")
        except ValueError:
            print("Invalid quantity")

    def _handle_buy(self):
        if self._selected_asset is None:
            print("Select an asset first")
            return
        try:
            qty = float(self.qty_entry.get())
            self.user.buy(self._selected_asset.symbol, qty, self.market)
            self._update_display()
            print(f"Bought {qty} {self._selected_asset.symbol}")
        except ValueError as e:
            print(e)

    def _handle_sell(self):
        if self._selected_asset is None:
            print("Select an asset first")
            return
        try:
            qty = float(self.qty_entry.get())
            self.user.sell(self._selected_asset.symbol, qty, self.market)
            self._update_display()
            print(f"Sold {qty} {self._selected_asset.symbol}")
        except ValueError as e:
            print(e)

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
            label.configure(text=f"${asset.price:,.2f}")
        self.tick_label.configure(text=f"Tick: {self.market.tick_count}")
        self.cash_label.configure(text=f"Cash: ${self.user.cash:,.2f}")
        if self._selected_asset:
            self._select_asset(self._selected_asset)
        self._update_portfolio_display()
        self._update_transaction_display()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = StockSimulatorApp()
    app.run()
    
