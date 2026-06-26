from engine import config

def test_load_risk_has_defaults():
    r = config.load_risk()
    assert r["max_position_pct"] == 0.10
    assert r["stop_pct"] == 0.07
    assert r["vix_full"] == 20

def test_load_watchlist_nonempty():
    wl = config.load_watchlist()
    assert "AAPL" in wl and all(t == t.strip() for t in wl)
