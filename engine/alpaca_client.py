import requests

class RealAlpacaClient:
    def __init__(self, creds):
        self.base = creds["endpoint"]
        self.h = {"APCA-API-KEY-ID": creds["key"], "APCA-API-SECRET-KEY": creds["secret"]}

    def _get(self, path, params=None):
        r = requests.get(self.base + path, headers=self.h, params=params, timeout=15)
        r.raise_for_status(); return r.json()

    def get_account(self): return self._get("/account")
    def get_positions(self): return self._get("/positions")
    def get_clock(self): return self._get("/clock")

    def get_bars(self, symbol, timeframe="1Day", limit=250):
        data = "https://data.alpaca.markets/v2/stocks/" + symbol + "/bars"
        r = requests.get(data, headers=self.h,
                         params={"timeframe": timeframe, "limit": limit}, timeout=15)
        r.raise_for_status(); return r.json().get("bars", [])

    def submit_bracket(self, symbol, qty, entry_type, stop_price, take_profit, client_order_id):
        body = {"symbol": symbol, "qty": str(qty), "side": "buy", "type": entry_type,
                "time_in_force": "gtc", "client_order_id": client_order_id,
                "order_class": "bracket", "stop_loss": {"stop_price": round(stop_price, 2)}}
        if take_profit:
            body["take_profit"] = {"limit_price": round(take_profit, 2)}
        r = requests.post(self.base + "/orders", headers=self.h, json=body, timeout=15)
        r.raise_for_status(); return r.json()

    def cancel_all_orders(self):
        requests.delete(self.base + "/orders", headers=self.h, timeout=15)

    def close_all_positions(self):
        requests.delete(self.base + "/positions", headers=self.h,
                        params={"cancel_orders": "true"}, timeout=15)
