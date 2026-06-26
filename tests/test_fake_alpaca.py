from engine.fake_alpaca import FakeAlpacaClient

def test_fake_submit_and_idempotency():
    c = FakeAlpacaClient(cash=100000, equity=100000)
    o1 = c.submit_bracket("AAPL", 10, "market", stop_price=180.0,
                          take_profit=None, client_order_id="bull-AAPL-2026-06-25")
    o2 = c.submit_bracket("AAPL", 10, "market", stop_price=180.0,
                          take_profit=None, client_order_id="bull-AAPL-2026-06-25")
    assert o1["id"] == o2["id"]          # same client_order_id -> no double place
    assert len(c.orders) == 1
    assert o1["stop_price"] == 180.0

def test_fake_close_all_flattens():
    c = FakeAlpacaClient(cash=0, equity=100000,
                         positions=[{"symbol": "AAPL", "qty": "10"}])
    c.close_all_positions()
    assert c.get_positions() == []
