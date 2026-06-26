import json
import datetime
from pathlib import Path
from engine import signals, rules, executor, killswitch

_DEFAULT_STATE = Path(__file__).resolve().parent.parent / "data" / "state.json"


def _iso_week(today_str):
    d = datetime.date.fromisoformat(today_str)
    y, w, _ = d.isocalendar()
    return "{}-W{:02d}".format(y, w)


def _load_state(state_path, current_week):
    p = Path(state_path)
    if p.exists():
        try:
            s = json.loads(p.read_text())
            if s.get("iso_week") == current_week:
                return s.get("new_trades", 0)
        except (json.JSONDecodeError, KeyError):
            pass
    return 0


def _save_state(state_path, iso_week, new_trades):
    p = Path(state_path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps({"iso_week": iso_week, "new_trades": new_trades}))


def _portfolio(client):
    acct = client.get_account()
    equity = float(acct["equity"])
    last = float(acct.get("last_equity", equity))
    day_pl = (equity - last) / last if last else 0.0
    open_syms = [p["symbol"] for p in client.get_positions()]
    return {"equity": equity, "cash": float(acct["cash"]), "open_symbols": open_syms,
            "new_trades_this_week": 0, "day_pl_pct": day_pl}


def run(client, watchlist, risk, flag_path, log_path, vix, today, blackouts=None,
        state_path=None):
    if state_path is None:
        state_path = _DEFAULT_STATE
    blackouts = blackouts or set()
    if killswitch.is_halted(flag_path):
        return {"placed": [], "skipped": [], "halted": True}

    clock = client.get_clock()
    if not clock["is_open"]:
        return {"placed": [], "skipped": [], "halted": False, "market_closed": True}

    iso_week = _iso_week(today)
    new_trades_count = _load_state(state_path, iso_week)

    port = _portfolio(client)
    port["new_trades_this_week"] = new_trades_count

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
                new_trades_count += 1
                _save_state(state_path, iso_week, new_trades_count)
            else:
                skipped.append(d)
    return {"placed": placed, "skipped": skipped, "halted": False}
