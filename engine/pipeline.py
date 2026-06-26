import json
from pathlib import Path
from engine import signals, rules, executor, killswitch


def _portfolio(client):
    acct = client.get_account()
    equity = float(acct["equity"])
    last = float(acct.get("last_equity", equity))
    day_pl = (equity - last) / last if last else 0.0
    open_syms = [p["symbol"] for p in client.get_positions()]
    return {"equity": equity, "cash": float(acct["cash"]), "open_symbols": open_syms,
            "new_trades_this_week": 0, "day_pl_pct": day_pl}


def run(client, watchlist, risk, flag_path, log_path, vix, today, blackouts=None):
    blackouts = blackouts or set()
    if killswitch.is_halted(flag_path):
        return {"placed": [], "skipped": [], "halted": True}
    port = _portfolio(client)
    placed, skipped = [], []
    with open(log_path, "a") as logf:
        for sym in watchlist:
            card = signals.build_signal_card(sym, client.get_bars(sym))
            d = rules.decide(card, port, vix, risk, blackout=(sym in blackouts))
            logf.write(json.dumps({"today": today, "vix": vix, **d}) + "\n")
            if d["go"]:
                executor.execute(d, client, today)
                placed.append(d)
                port["open_symbols"].append(sym)
                port["new_trades_this_week"] += 1
            else:
                skipped.append(d)
    return {"placed": placed, "skipped": skipped, "halted": False}
