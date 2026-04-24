from datetime import datetime
from tkinter import filedialog
from Models.factory import load_assets_from_csv
from Models.market import Market
from Models.user import User
import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ── Constants ────────────────────────────────────────────────────────────────

THEME = {
    "bg_dark":   "#1a1a2e",
    "bg_mid":    "#16213e",
    "bg_panel":  "#0f3460",
    "green":     "#00ff88",
    "cyan":      "#00ffff",
    "yellow":    "#ffff00",
    "red":       "#cc3333",
    "red_hover": "#aa2222",
    "muted":     "#aaaaaa",
    "dim":       "#888888",
    "buy_green": "#00aa55",
    "buy_hover": "#008844",
    "btn_blue":  "#0f3460",
    "btn_hover": "#16213e",
    "buy_bg":    "#0d2818",
    "sell_bg":   "#330000",
}

_MODES = {
    "Realistic":          (0.01,  5, 1.0),
    "Volatile":           (0.05,  8, 1.5),
    "Extremely Volatile": (0.15, 15, 2.5),
}

_CASH_PRESETS = [
    ("$10 K",      10_000),
    ("$50 K",      50_000),
    ("$100 K",    100_000),
    ("$500 K",    500_000),
    ("$1 M",    1_000_000),
    ("$10 M",  10_000_000),
]


def _fmt_qty(qty):
    return f"{qty:.2f}".rstrip("0").rstrip(".") if qty % 1 != 0 else str(int(qty))


def _pnl_style(value):
    """Return (sign_prefix, color) for a P&L value."""
    return ("+" if value >= 0 else "", THEME["green"] if value >= 0 else "#ff6666")


# ── Startup dialog ────────────────────────────────────────────────────────────

class StartupDialog:
    """Collects player name and starting cash before the simulator opens."""

    def __init__(self):
        self.result = None
        self._root = ctk.CTk()
        self._root.title("Stock Market Simulator")
        self._root.geometry("500x420")
        self._root.resizable(False, False)
        self._build()
        self._root.mainloop()

    def _build(self):
        ctk.CTkLabel(self._root, text="Stock Market Simulator",
                     font=("Arial", 24, "bold")).pack(pady=(30, 5))
        ctk.CTkLabel(self._root, text="Set up your session",
                     font=("Arial", 13), text_color=THEME["muted"]).pack(pady=(0, 20))

        form = ctk.CTkFrame(self._root, fg_color=THEME["bg_dark"], corner_radius=10)
        form.pack(fill="x", padx=30)

        ctk.CTkLabel(form, text="Player name", font=("Arial", 12),
                     text_color=THEME["muted"], anchor="w").pack(fill="x", padx=15, pady=(15, 2))
        self._name_entry = ctk.CTkEntry(form, placeholder_text="Player1", width=440)
        self._name_entry.pack(padx=15, pady=(0, 15))

        ctk.CTkLabel(form, text="Starting cash", font=("Arial", 12),
                     text_color=THEME["muted"], anchor="w").pack(fill="x", padx=15)

        presets = ctk.CTkFrame(form, fg_color="transparent")
        presets.pack(fill="x", padx=15, pady=5)
        for label, amount in _CASH_PRESETS:
            ctk.CTkButton(
                presets, text=label, width=65, height=28,
                fg_color=THEME["btn_blue"], hover_color=THEME["btn_hover"],
                font=("Arial", 11),
                command=lambda a=amount: self._set_cash(a),
            ).pack(side="left", padx=2)

        self._cash_entry = ctk.CTkEntry(form, placeholder_text="or type a custom amount", width=440)
        self._cash_entry.pack(padx=15, pady=(5, 15))

        self._error_label = ctk.CTkLabel(self._root, text="", font=("Arial", 11),
                                         text_color=THEME["red"])
        self._error_label.pack(pady=(12, 0))

        ctk.CTkButton(
            self._root, text="Start Simulation", width=200, height=40,
            fg_color=THEME["buy_green"], hover_color=THEME["buy_hover"],
            font=("Arial", 14, "bold"), command=self._submit,
        ).pack(pady=12)

    def _set_cash(self, amount):
        self._cash_entry.delete(0, "end")
        self._cash_entry.insert(0, str(amount))

    def _submit(self):
        name = self._name_entry.get().strip() or "Player1"
        raw = self._cash_entry.get().strip().replace(",", "").replace("$", "")
        try:
            cash = float(raw)
            if cash <= 0:
                raise ValueError
        except ValueError:
            self._error_label.configure(text="Enter a valid positive cash amount.")
            return
        self.result = (name, cash)
        self._root.destroy()


# ── Main app ──────────────────────────────────────────────────────────────────

class StockSimulatorApp:
    def __init__(self):
        dialog = StartupDialog()
        if dialog.result is None:
            raise SystemExit

        player_name, starting_cash = dialog.result

        self.assets = load_assets_from_csv("Data/assets.csv")
        self.market = Market(self.assets)
        self.user = User(player_name, starting_cash)
        self._running = False
        self._selected_asset = None
        self._price_labels = {}
        self._detail_price_label = None  # updated in-place on each tick

        self.root = ctk.CTk()
        self.root.title("Stock Market Simulator")
        self.root.geometry("1000x650")

        self._build_bottom_bar()

        self.tabs = ctk.CTkTabview(self.root)
        self.tabs.pack(expand=True, fill="both", padx=10, pady=(10, 0))
        self.market_tab = self.tabs.add("Market")
        self.portfolio_tab = self.tabs.add("Portfolio")
        self.transaction_tab = self.tabs.add("Transactions")

        self._build_market_tab()

        # Portfolio and transaction containers — just the persistent frame
        self.portfolio_frame = ctk.CTkFrame(self.portfolio_tab, fg_color=THEME["bg_panel"])
        self.portfolio_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.transaction_frame = ctk.CTkFrame(self.transaction_tab, fg_color=THEME["bg_panel"])
        self.transaction_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self._update_portfolio_display()
        self._update_transaction_display()

    # ── Bottom bar ────────────────────────────────────────────────────────────

    def _build_bottom_bar(self):
        bar = ctk.CTkFrame(self.root, height=50, fg_color=THEME["bg_dark"])
        bar.pack(fill="x", side="bottom", padx=10, pady=10)

        ctk.CTkButton(bar, text="▶ Play", width=80,
                      fg_color=THEME["btn_blue"], hover_color=THEME["btn_hover"],
                      command=self._play).pack(side="left", padx=10, pady=10)

        ctk.CTkButton(bar, text="⏸ Pause", width=80,
                      fg_color=THEME["btn_blue"], hover_color=THEME["btn_hover"],
                      command=self._pause).pack(side="left", padx=5, pady=10)

        self.tick_label = ctk.CTkLabel(bar, text="Tick: 0", font=("Arial", 14))
        self.tick_label.pack(side="left", padx=20)

        ctk.CTkLabel(bar, text="Mode:", font=("Arial", 13)).pack(side="left", padx=(20, 5))

        self.mode_selector = ctk.CTkSegmentedButton(
            bar, values=list(_MODES.keys()), command=self._set_mode, font=("Arial", 12))
        self.mode_selector.set("Realistic")
        self.mode_selector.pack(side="left", padx=5, pady=10)

        ctk.CTkButton(bar, text="⬆ Import CSV", width=110,
                      fg_color=THEME["btn_blue"], hover_color=THEME["btn_hover"],
                      command=self._import_assets).pack(side="left", padx=10, pady=10)

        self.status_label = ctk.CTkLabel(bar, text="", font=("Arial", 12),
                                         text_color=THEME["muted"])
        self.status_label.pack(side="left", padx=10)

        ctk.CTkButton(bar, text="📄 Report", width=90,
                      fg_color=THEME["btn_blue"], hover_color=THEME["btn_hover"],
                      command=self._generate_report).pack(side="right", padx=5, pady=10)

        self.pnl_label = ctk.CTkLabel(bar, text="P&L: $0.00", font=("Arial", 14),
                                      text_color=THEME["muted"])
        self.pnl_label.pack(side="right", padx=10)

        self.cash_label = ctk.CTkLabel(bar, text=f"Cash: ${self.user.cash:,.2f}",
                                       font=("Arial", 14), text_color=THEME["green"])
        self.cash_label.pack(side="right", padx=10)

    # ── Market tab ────────────────────────────────────────────────────────────

    def _build_market_tab(self):
        watchlist_frame = ctk.CTkFrame(self.market_tab, width=250, fg_color=THEME["bg_dark"])
        watchlist_frame.grid(row=0, column=0, sticky="ns", padx=(10, 5), pady=10)
        watchlist_frame.grid_propagate(False)
        ctk.CTkLabel(watchlist_frame, text="Watchlist", font=("Arial", 20, "bold")).pack(pady=(15, 10))
        self._watchlist_rows_frame = ctk.CTkFrame(watchlist_frame, fg_color="transparent")
        self._watchlist_rows_frame.pack(fill="both", expand=True)

        self.detail_frame = ctk.CTkFrame(self.market_tab, fg_color=THEME["bg_panel"])
        self.detail_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 10), pady=10)
        ctk.CTkLabel(self.detail_frame, text="Select an asset to view details",
                     font=("Arial", 18)).pack(expand=True)

        self.market_tab.grid_columnconfigure(1, weight=1)
        self.market_tab.grid_rowconfigure(0, weight=1)

        self._build_watchlist()

    def _build_watchlist(self):
        for widget in self._watchlist_rows_frame.winfo_children():
            widget.destroy()
        self._price_labels.clear()

        for asset in self.market.assets.values():
            row = ctk.CTkFrame(self._watchlist_rows_frame, fg_color=THEME["bg_mid"],
                               corner_radius=8, cursor="hand2")
            row.pack(fill="x", padx=8, pady=3)

            sym = ctk.CTkLabel(row, text=asset.symbol, font=("Arial", 14, "bold"), anchor="w")
            sym.pack(side="left", padx=(10, 5), pady=8)

            price_lbl = ctk.CTkLabel(row, text=f"${asset.price:.2f}", font=("Arial", 13),
                                     anchor="e", text_color=THEME["green"])
            price_lbl.pack(side="right", padx=(5, 10), pady=8)

            self._price_labels[asset.symbol] = price_lbl

            for w in (row, sym, price_lbl):
                w.bind("<Button-1>", lambda _, a=asset: self._select_asset(a))

    def _select_asset(self, asset):
        self._selected_asset = asset
        self._detail_price_label = None

        for widget in self.detail_frame.winfo_children():
            widget.destroy()

        ctk.CTkLabel(self.detail_frame, text=asset.name,
                     font=("Arial", 28, "bold")).pack(pady=(20, 5))
        ctk.CTkLabel(self.detail_frame, text=asset.symbol,
                     font=("Arial", 16), text_color=THEME["dim"]).pack(pady=(0, 15))

        self._detail_price_label = ctk.CTkLabel(
            self.detail_frame, text=f"${asset.price:,.2f}",
            font=("Arial", 36, "bold"), text_color=THEME["green"])
        self._detail_price_label.pack(pady=(0, 10))

        ctk.CTkLabel(self.detail_frame, text=f"Volatility: {asset.volatility}",
                     font=("Arial", 14), text_color=THEME["muted"]).pack(pady=2)
        if hasattr(asset, "sector"):
            ctk.CTkLabel(self.detail_frame, text=f"Sector: {asset.sector}",
                         font=("Arial", 14), text_color=THEME["muted"]).pack(pady=2)
        if hasattr(asset, "blockchain"):
            ctk.CTkLabel(self.detail_frame, text=f"Blockchain: {asset.blockchain}",
                         font=("Arial", 14), text_color=THEME["muted"]).pack(pady=2)

        trade_frame = ctk.CTkFrame(self.detail_frame, fg_color="transparent")
        trade_frame.pack(pady=20)
        self.qty_entry = ctk.CTkEntry(trade_frame, placeholder_text="Quantity", width=120)
        self.qty_entry.pack(side="left", padx=5)
        ctk.CTkButton(trade_frame, text="Buy", width=80,
                      fg_color=THEME["buy_green"], hover_color=THEME["buy_hover"],
                      command=lambda: self._handle_trade("buy")).pack(side="left", padx=5)
        ctk.CTkButton(trade_frame, text="Sell", width=80,
                      fg_color=THEME["red"], hover_color=THEME["red_hover"],
                      command=lambda: self._handle_trade("sell")).pack(side="left", padx=5)

        if len(asset.price_history) > 1:
            self._draw_chart(asset)

    def _draw_chart(self, asset):
        fig, ax = plt.subplots(figsize=(5, 2.5))
        fig.patch.set_facecolor(THEME["bg_panel"])
        ax.set_facecolor(THEME["bg_dark"])
        ax.plot(asset.price_history, color=THEME["green"], linewidth=1.5)
        ax.tick_params(colors=THEME["muted"], labelsize=8)
        ax.spines[:].set_color("#333355")
        ax.set_xlabel("Tick", color=THEME["muted"], fontsize=8)
        ax.set_ylabel("Price", color=THEME["muted"], fontsize=8)
        fig.tight_layout(pad=1.0)
        canvas = FigureCanvasTkAgg(fig, master=self.detail_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="x", padx=15, pady=(5, 15))
        plt.close(fig)

    # ── Portfolio tab ─────────────────────────────────────────────────────────

    def _update_portfolio_display(self):
        for widget in self.portfolio_frame.winfo_children():
            widget.destroy()

        ctk.CTkLabel(self.portfolio_frame, text="Portfolio",
                     font=("Arial", 28, "bold")).pack(pady=(20, 15))

        portfolio_value = self.user.portfolio.total_value()
        total_value = self.user.cash + portfolio_value
        pnl = self.user.total_pnl
        pnl_sign, pnl_color = _pnl_style(pnl)

        info_frame = ctk.CTkFrame(self.portfolio_frame, fg_color=THEME["bg_dark"], corner_radius=8)
        info_frame.pack(fill="x", padx=20, pady=10)
        ctk.CTkLabel(info_frame, text=f"Cash: ${self.user.cash:,.2f}",
                     font=("Arial", 16), text_color=THEME["green"]).pack(anchor="w", padx=15, pady=10)
        ctk.CTkLabel(info_frame, text=f"Holdings Value: ${portfolio_value:,.2f}",
                     font=("Arial", 16), text_color=THEME["cyan"]).pack(anchor="w", padx=15, pady=5)
        ctk.CTkLabel(info_frame, text=f"Total Value: ${total_value:,.2f}",
                     font=("Arial", 18, "bold"), text_color=THEME["yellow"]).pack(anchor="w", padx=15, pady=10)
        ctk.CTkLabel(info_frame, text=f"Overall P&L: {pnl_sign}${pnl:,.2f}",
                     font=("Arial", 16, "bold"), text_color=pnl_color).pack(anchor="w", padx=15, pady=10)

        if self.user.portfolio._holdings:
            ctk.CTkLabel(self.portfolio_frame, text="Holdings",
                         font=("Arial", 20, "bold")).pack(pady=(20, 10), anchor="w", padx=20)
            scroll = ctk.CTkScrollableFrame(self.portfolio_frame, fg_color=THEME["bg_dark"])
            scroll.pack(fill="both", expand=True, padx=20, pady=10)
            pnl_map = self.user.portfolio.unrealized_pnl_by_symbol()
            for symbol, holding in self.user.portfolio._holdings.items():
                self._holding_row(scroll, symbol, holding, pnl_map.get(symbol, 0.0))
        else:
            ctk.CTkLabel(self.portfolio_frame, text="Portfolio is empty",
                         font=("Arial", 16), text_color=THEME["dim"]).pack(pady=40)

    def _holding_row(self, parent, symbol, holding, h_pnl):
        asset = holding["asset"]
        qty = holding["quantity"]
        h_sign, h_color = _pnl_style(h_pnl)

        row = ctk.CTkFrame(parent, fg_color=THEME["bg_mid"], corner_radius=8)
        row.pack(fill="x", pady=5)
        ctk.CTkLabel(row, text=asset.name, font=("Arial", 14, "bold"),
                     anchor="w").pack(side="left", padx=10, pady=8, expand=True, fill="x")
        ctk.CTkLabel(row, text=f"{_fmt_qty(qty)} units", font=("Arial", 12),
                     text_color=THEME["muted"]).pack(side="left", padx=5, pady=8)
        ctk.CTkLabel(row, text=f"@ ${asset.price:,.2f}", font=("Arial", 12),
                     text_color=THEME["green"]).pack(side="left", padx=5, pady=8)
        ctk.CTkLabel(row, text=f"${asset.price * qty:,.2f}", font=("Arial", 13, "bold"),
                     text_color=THEME["cyan"]).pack(side="left", padx=5, pady=8)
        ctk.CTkLabel(row, text=f"{h_sign}${h_pnl:,.2f}", font=("Arial", 12, "bold"),
                     text_color=h_color).pack(side="left", padx=5, pady=8)
        ctk.CTkButton(row, text="Sell", width=60,
                      fg_color=THEME["red"], hover_color=THEME["red_hover"],
                      command=lambda s=symbol, q=qty: self._quick_sell(s, q)).pack(side="right", padx=10, pady=8)

    # ── Transactions tab ──────────────────────────────────────────────────────

    def _update_transaction_display(self):
        for widget in self.transaction_frame.winfo_children():
            widget.destroy()

        ctk.CTkLabel(self.transaction_frame, text="Transaction History",
                     font=("Arial", 28, "bold")).pack(pady=(20, 15))

        if not self.user._transactions.history:
            ctk.CTkLabel(self.transaction_frame, text="No transactions yet",
                         font=("Arial", 16), text_color=THEME["dim"]).pack(pady=40)
            return

        scroll = ctk.CTkScrollableFrame(self.transaction_frame, fg_color=THEME["bg_dark"])
        scroll.pack(fill="both", expand=True, padx=20, pady=10)
        for trans in self.user._transactions.history:
            self._transaction_row(scroll, trans)

    def _transaction_row(self, parent, trans):
        is_buy = trans["position"] == "buy"
        color = THEME["green"] if is_buy else "#ff6666"
        row = ctk.CTkFrame(parent, fg_color=THEME["buy_bg"] if is_buy else THEME["sell_bg"],
                           corner_radius=8)
        row.pack(fill="x", pady=5)
        ctk.CTkLabel(row,
                     text=f"{'BUY' if is_buy else 'SELL'} {_fmt_qty(trans['quantity'])}x {trans['asset'].symbol}",
                     font=("Arial", 13, "bold"), text_color=color,
                     anchor="w").pack(side="left", padx=10, pady=8, expand=True, fill="x")
        ctk.CTkLabel(row, text=f"@ ${trans['price']:,.2f} • Tick {trans['tick']}",
                     font=("Arial", 12), text_color=THEME["muted"]).pack(side="left", padx=5, pady=8)
        ctk.CTkLabel(row, text=f"${trans['quantity'] * trans['price']:,.2f}",
                     font=("Arial", 12, "bold"), text_color=color,
                     anchor="e").pack(side="right", padx=10, pady=8)

    # ── Trade handlers ────────────────────────────────────────────────────────

    def _handle_trade(self, action):
        if self._selected_asset is None:
            self._set_status("Select an asset first.", error=True)
            return
        try:
            qty = float(self.qty_entry.get())
            if action == "buy":
                self.user.buy(self._selected_asset.symbol, qty, self.market)
            else:
                self.user.sell(self._selected_asset.symbol, qty, self.market)
            self._update_display()
            verb = "Bought" if action == "buy" else "Sold"
            self._set_status(f"{verb} {_fmt_qty(qty)} {self._selected_asset.symbol}.")
        except ValueError as e:
            self._set_status(str(e), error=True)

    def _quick_sell(self, symbol, available_qty):
        dialog = ctk.CTkInputDialog(
            text=f"Enter quantity to sell (max: {available_qty:.2f}):", title="Sell")
        qty_str = dialog.get_input()
        if not qty_str:
            return
        try:
            qty = float(qty_str)
            if qty <= 0 or qty > available_qty:
                self._set_status("Invalid quantity.", error=True)
                return
            self.user.sell(symbol, qty, self.market)
            self._update_display()
            self._set_status(f"Sold {_fmt_qty(qty)} {symbol}.")
        except ValueError:
            self._set_status("Invalid quantity.", error=True)

    # ── Mode & import ─────────────────────────────────────────────────────────

    def _set_mode(self, mode):
        shock_prob, shock_mult, vol_mult = _MODES[mode]
        self.market.SHOCK_PROBABILITY = shock_prob
        self.market.SHOCK_MULTIPLIER = shock_mult
        self.market.volatility_multiplier = vol_mult
        self._set_status(f"Mode set to {mode}.")

    def _import_assets(self):
        path = filedialog.askopenfilename(
            title="Import assets CSV",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
        )
        if not path:
            return
        try:
            new_assets = load_assets_from_csv(path)
            self.market._assets.update(new_assets)
            self._build_watchlist()
            self._set_status(f"Imported {len(new_assets)} asset(s) from file.")
        except Exception as e:
            self._set_status(f"Import failed: {e}", error=True)

    # ── Simulation loop ───────────────────────────────────────────────────────

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

    # ── Display helpers ───────────────────────────────────────────────────────

    def _update_display(self):
        for symbol, label in self._price_labels.items():
            asset = self.market.get_asset(symbol)
            if asset:
                label.configure(text=f"${asset.price:,.2f}")

        self.tick_label.configure(text=f"Tick: {self.market.tick_count}")
        self.cash_label.configure(text=f"Cash: ${self.user.cash:,.2f}")

        pnl = self.user.total_pnl
        pnl_sign, pnl_color = _pnl_style(pnl)
        self.pnl_label.configure(text=f"P&L: {pnl_sign}${pnl:,.2f}", text_color=pnl_color)

        # Update only the price label in the detail panel — no full rebuild
        if self._detail_price_label and self._selected_asset:
            self._detail_price_label.configure(
                text=f"${self._selected_asset.price:,.2f}")

        self._update_portfolio_display()
        self._update_transaction_display()

    def _set_status(self, message, error=False):
        _, color = _pnl_style(0 if not error else -1)
        color = THEME["red"] if error else THEME["green"]
        self.status_label.configure(text=message, text_color=color)
        self.root.after(4000, lambda: self.status_label.configure(text=""))

    def _generate_report(self):
        path = filedialog.asksaveasfilename(
            title="Save Report",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialfile=f"report_tick{self.market.tick_count}.txt",
        )
        if not path:
            return

        pnl = self.user.total_pnl
        pnl_sign, _ = _pnl_style(pnl)
        pnl_map = self.user.portfolio.unrealized_pnl_by_symbol()

        lines = [
            "=" * 60,
            "  STOCK SIMULATOR — SESSION REPORT",
            "=" * 60,
            f"  Generated : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"  Player    : {self.user.name}",
            f"  Ticks     : {self.market.tick_count}",
            f"  Mode      : {self.mode_selector.get()}",
            "=" * 60,
            "",
            "SUMMARY",
            "-" * 40,
            f"  Starting cash  : ${self.user.starting_cash:>20,.2f}",
            f"  Current cash   : ${self.user.cash:>20,.2f}",
            f"  Holdings value : ${self.user.portfolio.total_value():>20,.2f}",
            f"  Net worth      : ${self.user.cash + self.user.portfolio.total_value():>20,.2f}",
            f"  Overall P&L    : {pnl_sign}${abs(pnl):>19,.2f}",
            "",
            "HOLDINGS",
            "-" * 40,
        ]

        if self.user.portfolio._holdings:
            for symbol, h in self.user.portfolio._holdings.items():
                asset = h["asset"]
                qty = h["quantity"]
                h_pnl = pnl_map.get(symbol, 0.0)
                h_sign, _ = _pnl_style(h_pnl)
                lines.append(
                    f"  {asset.name:<20} {_fmt_qty(qty):>10} units  "
                    f"@ ${asset.price:>12,.2f}  value ${asset.price * qty:>14,.2f}"
                    f"  P&L {h_sign}${h_pnl:>12,.2f}"
                )
        else:
            lines.append("  (no holdings)")

        lines += ["", "TRANSACTION HISTORY", "-" * 40]

        if self.user._transactions.history:
            for t in self.user._transactions.history:
                action = "BUY " if t["position"] == "buy" else "SELL"
                lines.append(
                    f"  Tick {t['tick']:<6} {action}  {_fmt_qty(t['quantity']):>10} x "
                    f"{t['asset'].symbol:<6} @ ${t['price']:>12,.2f}"
                    f"  total ${t['quantity'] * t['price']:>14,.2f}"
                )
        else:
            lines.append("  (no transactions)")

        lines += ["", "=" * 60]

        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write("\n".join(lines))
            self._set_status("Report saved.")
        except OSError as e:
            self._set_status(f"Could not save: {e}", error=True)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = StockSimulatorApp()
    app.run()
