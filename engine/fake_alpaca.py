class FakeAlpacaClient:
    def __init__(self, cash=100000, equity=100000, positions=None, bars=None, is_open=True):
        self._cash = cash; self._equity = equity; self._last_equity = equity
        self._positions = positions or []
        self._bars = bars or {}
        self._is_open = is_open
        self.orders = []
        self.cancelled = False

    def get_account(self):
        return {"cash": str(self._cash), "equity": str(self._equity),
                "last_equity": str(self._last_equity), "status": "ACTIVE"}

    def get_positions(self): return list(self._positions)

    def get_bars(self, symbol, timeframe="1Day", limit=250):
        return self._bars.get(symbol, [])

    def get_clock(self): return {"is_open": self._is_open}

    def submit_bracket(self, symbol, qty, entry_type, stop_price, take_profit, client_order_id):
        for o in self.orders:
            if o["client_order_id"] == client_order_id:
                return o
        order = {"id": f"fake-{len(self.orders)+1}", "client_order_id": client_order_id,
                 "symbol": symbol, "qty": qty, "type": entry_type,
                 "stop_price": stop_price, "take_profit": take_profit, "status": "accepted"}
        self.orders.append(order)
        return order

    def cancel_all_orders(self): self.cancelled = True; self.orders = []
    def close_all_positions(self): self._positions = []
