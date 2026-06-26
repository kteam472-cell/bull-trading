from engine import analysts, rules

RISK = {"max_position_pct": 0.10, "stop_pct": 0.07, "vix_full": 20, "vix_half": 30,
        "max_new_per_week": 3, "daily_loss_cap_pct": 0.03, "cash_floor_pct": 0.20}
PORT = {"equity": 100000, "cash": 100000, "open_symbols": [],
        "new_trades_this_week": 0, "day_pl_pct": 0.0}
CARD = {"symbol": "AAPL", "last": 100.0, "rsi14": 40, "sma20": 99, "sma50": 98,
        "sma200": 90, "vol_ratio": 1.2, "pct_52w": 0.6}

def fake_llm(prompt): return '{"stance": "bearish", "note": "overbought vibes"}'

def test_advice_does_not_change_decision():
    before = rules.decide(dict(CARD), PORT, 15, RISK, False)
    annotated = analysts.annotate(dict(CARD), fake_llm)
    after = rules.decide(annotated, PORT, 15, RISK, False)
    assert before == after          # advisory only; never gates
    assert annotated["advice"]["stance"] == "bearish"
