from engine import signals

def test_rsi_all_gains_near_100():
    closes = [float(i) for i in range(1, 30)]   # monotonic up
    assert signals.rsi(closes, 14) > 95

def test_sma_simple():
    assert signals.sma([10, 20, 30], 3) == 20.0

def test_build_signal_card_keys():
    bars = [{"c": 100 + i, "h": 101 + i, "l": 99 + i, "v": 1000} for i in range(60)]
    card = signals.build_signal_card("AAPL", bars)
    assert card["symbol"] == "AAPL"
    assert card["sma20"] is not None and card["sma200"] is None  # only 60 bars
    assert 0 <= card["rsi14"] <= 100
