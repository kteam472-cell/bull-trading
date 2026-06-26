from engine import signals, rules

def run(bars_by_symbol, spy_bars, risk, friction_bps=10.0):
    fr = friction_bps / 10000.0
    pnls = []
    for sym, bars in bars_by_symbol.items():
        i = 200
        while i < len(bars) - 1:
            card = signals.build_signal_card(sym, bars[:i+1])
            port = {"equity": 100000, "cash": 100000, "open_symbols": [],
                    "new_trades_this_week": 0, "day_pl_pct": 0.0}
            d = rules.decide(card, port, vix=15, risk=risk, blackout=False)
            if not d["go"]:
                i += 1; continue
            entry = bars[i]["c"] * (1 + fr)
            stop = d["stop_price"]
            j = i + 1; exit_px = bars[-1]["c"]
            while j < len(bars):
                if bars[j]["l"] <= stop:
                    exit_px = stop; break
                c2 = signals.build_signal_card(sym, bars[:j+1])
                if c2["sma50"] and c2["last"] < c2["sma50"]:
                    exit_px = bars[j]["c"]; break
                j += 1
            exit_px *= (1 - fr)
            pnls.append((exit_px - entry) / entry)
            i = j + 1
    spy_ret = (spy_bars[-1]["c"] - spy_bars[0]["c"]) / spy_bars[0]["c"]
    if not pnls:
        return {"trades": 0, "win_rate": 0.0, "expectancy": 0.0,
                "total_return": 0.0, "spy_return": spy_ret, "beats_spy": False}
    wins = [p for p in pnls if p > 0]
    total = sum(pnls)
    return {"trades": len(pnls), "win_rate": len(wins)/len(pnls),
            "expectancy": total/len(pnls), "total_return": total,
            "spy_return": spy_ret, "beats_spy": total > spy_ret}
