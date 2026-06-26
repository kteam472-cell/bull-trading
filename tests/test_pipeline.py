import json
from engine import pipeline
from engine.fake_alpaca import FakeAlpacaClient

RISK = {"max_position_pct": 0.10, "stop_pct": 0.07, "vix_full": 20, "vix_half": 30,
        "max_new_per_week": 3, "daily_loss_cap_pct": 0.03, "cash_floor_pct": 0.20}

def _bars(trend_up=True):
    """Generate 210 realistic bars.

    Uptrend: price rises with periodic pullbacks (2 up, 1 back).
    Produces final close above SMA50 and SMA200, RSI(14) well below 70.
    Downtrend: gentle continuous decline — last close falls below SMA50.
    """
    closes = []
    if trend_up:
        price = 50.0
        for i in range(210):
            if i % 3 == 2:
                price *= 0.98   # pullback day keeps RSI realistic
            else:
                price *= 1.015  # two up days
            closes.append(price)
    else:
        price = 200.0
        for i in range(210):
            price *= 0.998  # gentle downtrend
            closes.append(price)
    return [{"c": c, "h": c * 1.01, "l": c * 0.99, "v": 1000} for c in closes]

def test_pipeline_places_on_uptrend_and_logs(tmp_path):
    c = FakeAlpacaClient(cash=100000, equity=100000, bars={"AAPL": _bars(True)})
    flag = tmp_path / "HALT"; log = tmp_path / "decisions.jsonl"
    out = pipeline.run(c, ["AAPL"], RISK, flag, log, vix=15, today="2026-06-25")
    assert "AAPL" in [o["symbol"] for o in out["placed"]]
    assert log.exists() and len(log.read_text().strip().splitlines()) == 1
    rec = json.loads(log.read_text().splitlines()[0])
    assert rec["go"] is True and rec["symbol"] == "AAPL"

def test_pipeline_short_circuits_when_halted(tmp_path):
    flag = tmp_path / "HALT"; flag.write_text("halted"); log = tmp_path / "d.jsonl"
    c = FakeAlpacaClient(bars={"AAPL": _bars(True)})
    out = pipeline.run(c, ["AAPL"], RISK, flag, log, vix=15, today="2026-06-25")
    assert out["halted"] is True and out["placed"] == []


# FIX 2: weekly new-trade count persists across runs
def test_weekly_count_accumulates_across_runs(tmp_path):
    """Same week: second run is blocked because persisted count == max_new_per_week=1."""
    risk_1 = dict(RISK, max_new_per_week=1)
    bars = {"AAPL": _bars(True), "MSFT": _bars(True)}
    flag = tmp_path / "HALT"
    log = tmp_path / "decisions.jsonl"
    state = tmp_path / "state.json"

    # Run 1: AAPL placed, count saved to 1
    c1 = FakeAlpacaClient(cash=100000, equity=100000, bars=bars)
    out1 = pipeline.run(c1, ["AAPL"], risk_1, flag, log, vix=15,
                        today="2026-06-23", state_path=state)
    assert "AAPL" in [o["symbol"] for o in out1["placed"]], "Run 1 should place AAPL"

    # Run 2 same week: MSFT should be blocked (count already at max)
    c2 = FakeAlpacaClient(cash=100000, equity=100000, bars=bars)
    out2 = pipeline.run(c2, ["MSFT"], risk_1, flag, log, vix=15,
                        today="2026-06-24", state_path=state)
    assert out2["placed"] == [], "Run 2 same week should be blocked by persisted count"


def test_weekly_count_resets_in_new_week(tmp_path):
    """New ISO week: count resets so a trade is allowed again."""
    risk_1 = dict(RISK, max_new_per_week=1)
    bars = {"AAPL": _bars(True), "MSFT": _bars(True)}
    flag = tmp_path / "HALT"
    log = tmp_path / "decisions.jsonl"
    state = tmp_path / "state.json"

    # Run in week W25 (2026-06-15 is Mon of W25)
    c1 = FakeAlpacaClient(cash=100000, equity=100000, bars=bars)
    out1 = pipeline.run(c1, ["AAPL"], risk_1, flag, log, vix=15,
                        today="2026-06-15", state_path=state)
    assert "AAPL" in [o["symbol"] for o in out1["placed"]], "Week W25 run should place AAPL"

    # Run in week W26 (2026-06-22 is Mon of W26): new week resets count, MSFT allowed
    c2 = FakeAlpacaClient(cash=100000, equity=100000, bars=bars)
    out2 = pipeline.run(c2, ["MSFT"], risk_1, flag, log, vix=15,
                        today="2026-06-22", state_path=state)
    assert "MSFT" in [o["symbol"] for o in out2["placed"]], "Week W26 run should place MSFT"


# FIX 3: market-open guard
def test_pipeline_skips_when_market_closed(tmp_path):
    """Nothing placed when clock says market is closed."""
    c = FakeAlpacaClient(cash=100000, equity=100000,
                         bars={"AAPL": _bars(True)}, is_open=False)
    flag = tmp_path / "HALT"
    log = tmp_path / "decisions.jsonl"
    out = pipeline.run(c, ["AAPL"], RISK, flag, log, vix=15, today="2026-06-25")
    assert out["placed"] == []
    assert out["market_closed"] is True
    assert out["halted"] is False
