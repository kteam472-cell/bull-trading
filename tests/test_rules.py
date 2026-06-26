from engine import rules

RISK = {"max_position_pct": 0.10, "stop_pct": 0.07, "vix_full": 20, "vix_half": 30,
        "max_new_per_week": 3, "daily_loss_cap_pct": 0.03, "cash_floor_pct": 0.20}
PORT = {"equity": 100000, "cash": 100000, "open_symbols": [],
        "new_trades_this_week": 0, "day_pl_pct": 0.0}

def card(**kw):
    base = {"symbol": "AAPL", "last": 100.0, "rsi14": 40, "sma20": 99, "sma50": 98,
            "sma200": 90, "vol_ratio": 1.2, "pct_52w": 0.6}
    base.update(kw); return base

def test_go_on_uptrend_sets_whole_share_qty_and_stop():
    d = rules.decide(card(), PORT, vix=15, risk=RISK, blackout=False)
    assert d["go"] is True
    assert d["qty"] == 100              # 10% of 100k / $100 = 100 whole shares
    assert abs(d["stop_price"] - 93.0) < 1e-6   # 7% below 100
    assert d["entry_type"] == "market"

def test_halt_when_vix_defense():
    d = rules.decide(card(), PORT, vix=35, risk=RISK, blackout=False)
    assert d["go"] is False and "vix" in " ".join(d["reasons"]).lower()

def test_half_size_in_caution_band():
    d = rules.decide(card(), PORT, vix=25, risk=RISK, blackout=False)
    assert d["qty"] == 50              # half of 100

def test_blackout_blocks():
    d = rules.decide(card(), PORT, vix=15, risk=RISK, blackout=True)
    assert d["go"] is False

def test_downtrend_no_go():
    d = rules.decide(card(last=100, sma50=110, sma200=120), PORT, vix=15, risk=RISK, blackout=False)
    assert d["go"] is False

def test_daily_loss_cap_blocks_new():
    p = {**PORT, "day_pl_pct": -0.04}
    assert rules.decide(card(), p, vix=15, risk=RISK, blackout=False)["go"] is False

def test_max_new_per_week_blocks():
    p = {**PORT, "new_trades_this_week": 3}
    assert rules.decide(card(), p, vix=15, risk=RISK, blackout=False)["go"] is False

def test_already_open_no_duplicate():
    p = {**PORT, "open_symbols": ["AAPL"]}
    assert rules.decide(card(), p, vix=15, risk=RISK, blackout=False)["go"] is False

def test_cash_floor_blocks():
    p = {**PORT, "cash": 15000}   # below 20% floor of 100k
    assert rules.decide(card(), p, vix=15, risk=RISK, blackout=False)["go"] is False

def test_too_expensive_for_whole_share_no_go():
    # price so high that <1 whole share fits the 10% cap
    d = rules.decide(card(last=20000), PORT, vix=15, risk=RISK, blackout=False)
    assert d["go"] is False and "whole share" in " ".join(d["reasons"]).lower()
