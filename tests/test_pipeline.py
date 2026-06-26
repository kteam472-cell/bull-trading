import json
from engine import pipeline
from engine.fake_alpaca import FakeAlpacaClient

RISK = {"max_position_pct": 0.10, "stop_pct": 0.07, "vix_full": 20, "vix_half": 30,
        "max_new_per_week": 3, "daily_loss_cap_pct": 0.03, "cash_floor_pct": 0.20}

def _bars(trend_up=True):
    return [{"c": (100 + i if trend_up else 200 - i), "h": 101 + i, "l": 98 + i, "v": 1000}
            for i in range(210)]

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
