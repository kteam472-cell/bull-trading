from engine import executor
from engine.fake_alpaca import FakeAlpacaClient

GO = {"go": True, "symbol": "AAPL", "qty": 100, "entry_type": "market",
      "stop_price": 93.0, "reasons": []}

def test_execute_places_bracket_with_idempotent_id():
    c = FakeAlpacaClient()
    o = executor.execute(GO, c, "2026-06-25")
    assert o["client_order_id"] == "bull-AAPL-2026-06-25"
    assert o["stop_price"] == 93.0
    # second call same day -> no double place
    executor.execute(GO, c, "2026-06-25")
    assert len(c.orders) == 1

def test_nogo_places_nothing():
    c = FakeAlpacaClient()
    assert executor.execute({"go": False, "symbol": "AAPL"}, c, "2026-06-25") is None
    assert len(c.orders) == 0

def test_refuses_without_stop():
    c = FakeAlpacaClient()
    bad = {**GO, "stop_price": None}
    try:
        executor.execute(bad, c, "2026-06-25"); assert False
    except ValueError:
        assert len(c.orders) == 0
