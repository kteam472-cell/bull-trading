def _entry_signal_ok(card):
    # simple, testable trend filter: price above 50 & 200 SMA, RSI not overbought
    if card["last"] is None or card["sma50"] is None: return False
    if card["sma200"] is not None and card["last"] < card["sma200"]: return False
    if card["last"] < card["sma50"]: return False
    if card["rsi14"] is not None and card["rsi14"] > 70: return False
    return True

def decide(card, portfolio, vix, risk, blackout):
    reasons = []
    def no(msg):
        reasons.append(msg)
        return {"go": False, "symbol": card["symbol"], "qty": 0,
                "entry_type": "market", "stop_price": None, "reasons": reasons}

    if blackout: return no("earnings/macro blackout window")
    if vix > risk["vix_half"]: return no(f"vix {vix} > defense threshold")
    if portfolio["day_pl_pct"] <= -risk["daily_loss_cap_pct"]: return no("daily loss cap hit")
    if portfolio["new_trades_this_week"] >= risk["max_new_per_week"]: return no("max new positions/week")
    if card["symbol"] in portfolio["open_symbols"]: return no("already holding symbol")
    if portfolio["cash"] < risk["cash_floor_pct"] * portfolio["equity"]: return no("cash floor")
    if not _entry_signal_ok(card): return no("entry signal not met (trend/RSI)")

    size_pct = risk["max_position_pct"]
    if vix >= risk["vix_full"]: size_pct *= 0.5   # caution band: half size
    dollars = size_pct * portfolio["equity"]
    qty = int(dollars // card["last"])             # whole shares only
    if qty < 1: return no("price too high for >=1 whole share within size cap")

    stop_price = round(card["last"] * (1 - risk["stop_pct"]), 2)
    reasons.append(f"trend ok, rsi {card['rsi14']}, size {size_pct:.0%}")
    return {"go": True, "symbol": card["symbol"], "qty": qty,
            "entry_type": "market", "stop_price": stop_price, "reasons": reasons}
