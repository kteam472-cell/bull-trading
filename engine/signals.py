def sma(closes, period):
    if len(closes) < period:
        return None
    return sum(closes[-period:]) / period


def rsi(closes, period=14):
    if len(closes) <= period:
        return None
    gains, losses = [], []
    for i in range(1, len(closes)):
        d = closes[i] - closes[i - 1]
        gains.append(max(d, 0))
        losses.append(max(-d, 0))
    avg_g = sum(gains[-period:]) / period
    avg_l = sum(losses[-period:]) / period
    if avg_l == 0:
        return 100.0
    rs = avg_g / avg_l
    return 100 - (100 / (1 + rs))


def build_signal_card(symbol, bars):
    closes = [b["c"] for b in bars]
    vols = [b["v"] for b in bars]
    last = closes[-1] if closes else None
    hi = max((b["h"] for b in bars), default=None)
    lo = min((b["l"] for b in bars), default=None)
    pct_52w = None
    if last is not None and hi is not None and lo is not None and hi > lo:
        pct_52w = (last - lo) / (hi - lo)
    vol_ratio = None
    if len(vols) >= 20 and sum(vols[-20:]) > 0:
        vol_ratio = vols[-1] / (sum(vols[-20:]) / 20)
    return {
        "symbol": symbol,
        "last": last,
        "rsi14": rsi(closes, 14),
        "sma20": sma(closes, 20),
        "sma50": sma(closes, 50),
        "sma200": sma(closes, 200),
        "vol_ratio": vol_ratio,
        "pct_52w": pct_52w,
    }
