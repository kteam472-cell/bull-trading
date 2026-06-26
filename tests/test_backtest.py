from engine import backtest

RISK = {"max_position_pct": 0.10, "stop_pct": 0.07, "vix_full": 20, "vix_half": 30,
        "max_new_per_week": 999, "daily_loss_cap_pct": 1.0, "cash_floor_pct": 0.0}


def _realistic_up_bars(n=260):
    """Cyclic up/pullback bars (2 up days, 1 pullback) over n bars.

    Mirrors test_pipeline._bars — produces last > sma50 > sma200 and rsi14 <= 68,
    so the rule engine can actually trigger a GO signal.
    """
    price = 50.0
    closes = []
    for i in range(n):
        if i % 3 == 2:
            price *= 0.98   # pullback day keeps RSI realistic
        else:
            price *= 1.015  # two up days
        closes.append(price)
    return [{"c": c, "h": c * 1.01, "l": c * 0.99, "v": 1000} for c in closes]


def test_backtest_runs_and_reports_metrics():
    up = _realistic_up_bars(260)
    spy = [{"c": 400 + i * 0.1, "h": 401, "l": 399, "v": 1} for i in range(260)]
    res = backtest.run({"AAPL": up}, spy, RISK, friction_bps=10.0)
    assert res["trades"] >= 1
    assert "expectancy" in res and "beats_spy" in res
    assert isinstance(res["beats_spy"], bool)
