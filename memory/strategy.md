# Bull Trading Strategy — Knowledge Base
*Last updated: 2026-06-09 | Version: 1.0 (research build) | Account: Alpaca Paper*

---

## CORE PHILOSOPHY

Beat the S&P 500. That is the only benchmark that matters. A 10% return when the S&P returns 15% is failure. An 8% return when the S&P returns -5% is success.

Every trade requires: (1) a documented thesis, (2) a defined entry, (3) a defined exit (both profit target and stop loss), and (4) a position size calculated against max risk rules. No exceptions.

**Three-filter entry checklist (all required):**
1. Market regime is favorable (VIX check — see Section 1)
2. Sector is in the right economic cycle phase
3. Individual stock clears the fundamentals + technical checklist

---

## SECTION 1 — MARKET REGIME DETECTION (VIX)

The VIX is the first thing checked each session. It determines which mode Bull operates in.

| VIX Level | Market Regime | Mode |
|-----------|--------------|------|
| Below 15 | Calm, low fear | OFFENSE — full position sizing, growth/momentum plays |
| 15–20 | Normal | OFFENSE — standard playbook, slightly tighter stops |
| 20–30 | Elevated uncertainty | CAUTION — trade at half size (5% per position = $12.50), high-quality names only, no speculative plays |
| 30–40 | High fear / correction | CAUTION — reduce new positions by 50%, stick to high-quality names only, no new longs on speculative names |
| Above 40 | Crisis / extreme fear | DEFENSE — hold cash, only buy VIX-confirmed reversals at extreme oversold readings |

**Historical context:** VIX averages around 19–20 long-term. Spikes above 30 have historically been buying opportunities in retrospect (2020 COVID spike to 82, 2018 VIXplosion to 37, 2008–2009 sustained above 40). The problem is timing the re-entry. Rule: wait for VIX to fall back below 30 before initiating new positions after a spike.

---

## SECTION 2 — SECTOR ROTATION BY ECONOMIC CYCLE

*Per Fidelity sector rotation framework + academic research (Stangl et al.)*

### Stage 1: Early Recovery (recession just ended)
**Outperforming sectors:** Consumer Discretionary, Financials
- Banks benefit from rate cuts and renewed lending
- Consumers returning to non-essential spending
- Historical outperformance vs. S&P: +8–15% in first 12 months of recovery
- **Sector ETFs:** XLY (Consumer Discretionary), XLF (Financials)

### Stage 2: Mid-Cycle Expansion (growth accelerating)
**Outperforming sectors:** Technology, Industrials, Communication Services
- Corporate spending picks up, IT budgets expand
- Infrastructure and industrial production expand
- Historical edge: sector rotation into tech/industrials has delivered 1–3% annualized excess return over SPY in large-scale backtests
- **Sector ETFs:** XLK (Tech), XLI (Industrials)

### Stage 3: Late Cycle (growth peaking, rates elevated)
**Outperforming sectors:** Energy, Materials, Real Estate (early in late cycle)
- Input cost inflation favors commodity producers
- Rising rates still manageable for real assets
- **Sector ETFs:** XLE (Energy), XLB (Materials)

### Stage 4: Recession
**Outperforming sectors:** Utilities, Consumer Staples, Healthcare
- Revenue stable regardless of economic conditions
- Historically outperformed S&P by 15–25% during recessions (2008–2009 data)
- **Sector ETFs:** XLU (Utilities), XLP (Staples), XLV (Healthcare)

**Practical rule:** Before entering any position, confirm which cycle phase the economy is likely in. Betting on tech during a recession is swimming upstream.

---

## SECTION 3 — SEASONAL PATTERNS

*Per Bespoke Investment Group, Seasonality360, and decades of S&P data*

### Monthly Return Tendencies (S&P 500 historical averages)
| Month | Avg Return | Notes |
|-------|-----------|-------|
| January | +1.0% | "January Effect" weakened for large caps; still holds for small caps |
| February | +0.1% | Weakest winter month |
| March | +1.0% | Recovery from Feb weakness |
| April | +1.5% | Historically one of the strongest months |
| May | +0.2% | Start of weak season ("Sell in May") |
| June | +0.0% | Weak |
| July | +1.0% | Mid-summer bounce |
| August | -0.1% | Historically negative on average |
| September | -0.7% | Worst month of the year — consistently negative across decades |
| October | +0.8% | Volatile but average is positive; contains some historic crashes |
| November | +1.7% | Strongest month — post-election clarity, year-end positioning |
| December | +1.5% | Santa Claus rally tendency |

**"Sell in May" (May–October) vs "Hold" (November–April):**
- November–April 6-month period averages significantly higher returns than May–October
- Long-term data supports the pattern; however, the gap has narrowed since widespread awareness
- **Practical rule:** Raise cash allocations and tighten stops entering May. Reduce defensive bias entering November.

**September rule:** September is the single worst month historically. Entering new long positions in September requires an especially strong individual thesis. When in doubt, wait for October.

---

## SECTION 4 — EARNINGS PLAYS

### Pre-Earnings Run-Up
- Some stocks exhibit directional bias in the 5–10 days before earnings based on sector momentum, analyst revision trends, and institutional positioning
- The effect is variable — not a universal setup. Best observed in: (a) stocks with recent upward analyst revisions, (b) sector momentum, (c) institutional positioning confirmed via options flow
- **Rule:** Do not blindly buy pre-earnings run-ups. Only enter if: analyst consensus has revised upward in the past 2 weeks AND the sector is in its favorable cycle phase AND the stock is not already extended (RSI below 65)

### Implied Volatility (IV) Crush Post-Earnings
- IV expands aggressively in the days leading up to earnings as options market prices in uncertainty
- Post-earnings, IV collapses regardless of whether the stock beats or misses (IV crush)
- **For paper trading:** Avoid holding through earnings unless the thesis specifically calls for it. The gap risk is unmanageable with a -7% hard stop.
- If Bull holds through earnings, set a mental stop at the implied move — if the stock opens outside the expected range, reassess immediately.

---

## SECTION 5 — TECHNICAL SETUPS WITH DOCUMENTED EDGE

### 5a. RSI Oversold Bounce (RSI < 30)
- Simple buy-below-30, sell-above-70 strategies show mixed results in isolation
- **Improved setup (higher win rate):** Wait for RSI to cross back ABOVE 30 after hitting oversold (confirmation signal). This filter increases win rate by approximately 15–20% vs. buying at the touch.
- Using RSI as pullback tool within established uptrends: win rate 60–70%
- Multi-timeframe confirmation (daily RSI oversold + weekly trend intact): 65–75% win rate in backtests
- **Rule:** RSI < 30 alone = note it. RSI crosses back above 30 in an established uptrend = consider entry. Confirm with volume above 20-day average.

### 5b. 50-Day Moving Average Bounce
- In established uptrends (price above 200-day MA), pullbacks to the 50-day MA are historically high-probability entry points
- **Rule:** Price tags 50-day MA, holds the level on at least 1 candle, volume on the bounce day exceeds 20-day average → valid entry
- Stops: just below the 50-day MA (-3% max)

### 5c. Golden Cross (50-day MA crosses above 200-day MA)
- Bullish long-term signal — short-to-medium term momentum shift confirmed
- **Historical performance:** The golden cross has produced positive forward returns over 6–12 months approximately 70% of the time in S&P 500 history
- **Limitation:** Lagging indicator. By the time it fires, the stock may have already moved 15–20%. Use as a filter, not a buy trigger.
- **Rule:** Golden cross = confirms the sector/stock is in an uptrend. Use as a background condition, not an entry signal on its own.

### 5d. 52-Week High Breakout (with Volume)
- Stocks breaking above 52-week highs with volume exceeding 150% of the 20-day average continue upward 72% of the time, averaging +11.4% over 31 trading days (Journal of Financial Markets research)
- Rejection-retest-breakout pattern (price touches high, pulls back 3–5%, then breaks through on high volume) = 76% win rate in documented studies
- VIX condition matters: win rate is 68% during VIX < 18, lower in higher-volatility environments
- **False breakout filter:** 31% of breakouts fail within 3 days; 78% of failures occur on below-average volume. If volume does not exceed the 20-day average on the breakout day, wait for confirmation.
- **Rule:** 52-week high breakout + volume above 150% of 20-day average + VIX below 20 = high-quality setup. Enter on the breakout candle or the first pullback day.

---

## SECTION 6 — FUNDAMENTALS CHECKLIST

Run this before entering any individual stock position:

| Factor | Threshold | Notes |
|--------|-----------|-------|
| P/E vs. sector | Below sector median, or growth-justified premium | Don't pay 40x for a 10% grower |
| Revenue growth | 10%+ YoY preferred; 5% minimum | Flat revenue = no growth thesis |
| Debt-to-equity | Below 1.5 for non-financial companies | Highly leveraged companies crater in rate hikes |
| Earnings trend | 2+ consecutive beats preferred | Pattern of beats = management execution |
| Insider buying | Cluster buying (3+ insiders) in past 3 months | Insiders buying cluster → 7.8% avg outperformance next 12 months vs. sellers (academic data) |
| Analyst revisions | Upward estimate revisions in past 30 days | Forward-looking signal |
| Free cash flow | FCF positive preferred | Earnings without FCF = accounting, not cash |

**Insider buying evidence:** Firms with extensive insider purchases in prior 6 months outperform companies with extensive insider sales by 7.8% over the next 12 months. Wharton research shows ~25% of abnormal returns accrue within the first 5 days of the trade and 50% within the first month. Signal is strongest in financial firms, moderate in utilities, weakest in tech.

**Source:** InsideArbitrage academic research index; Lakonishok & Lee (2001)

---

## SECTION 7 — RISK MANAGEMENT (NON-NEGOTIABLE)

### Account Details
- **Starting capital:** $250 live (Alpaca live account)
- **Alpaca supports fractional shares** — no minimum share size. Buy $12.50 of NVDA if that's the right size.
- **Benchmark:** Beat SPY. That is the only goal.

### Position Sizing ($250 account)
- **Max position size: 10% of portfolio = $25 per position**
- Typical position: $15–$25 (use fractional shares, no minimum)
- Max 5 open positions simultaneously ($125 deployed, $125 cash minimum)
- Do NOT scale up position size to compensate for small account — the math must hold regardless of account size

### Cash Reserve
- **Minimum $50 in cash at all times** — never fully deployed
- This buffer ensures you can respond to opportunities and absorb costs
- If cash drops below $50, do not open new positions until a position closes

### PDT Rule (Pattern Day Trader)
- Accounts under $25,000 are limited to **3 day trades per rolling 5 business days**
- A "day trade" = opening AND closing the same position within the same calendar day
- Swing trading primary = this rarely triggers (you hold overnight)
- **Bull must track day trades used this week.** If 2 day trades already used this week → flag in Telegram before any same-day close. Do NOT use the 3rd day trade without notifying Zack first.
- Day trade count resets after 5 business days

### Hard Stop: -7%
- Every position gets a hard stop at -7% from entry price
- **Rationale:** A -7% stop on a $25 position = -$1.75 max loss. Survivable.
- Set the stop at entry. Do not move it down.
- If a position hits -7%, exit immediately. No holding for a recovery.

### Daily Loss Limit
- **$12.50 per day (5% of account)**
- If realized + unrealized losses reach -$12.50 in one trading session, close all positions and stop trading for that day
- Log the day as "max loss day" in research-log.md

### Trailing Stop: 10%
- Once a position is up 10%+, move the stop to breakeven
- Once up 20%+, trail the stop at 10% below the high-water mark

### Concentration Limits
- Max 2 positions in the same sector simultaneously
- Max $50 (20% of account) in any single sector
- Cash is a position — if VIX is above 30, staying in cash is the right trade; between 20–30, trade at half size

---

## SECTION 8 — BEATING THE S&P (THE GOAL)

**S&P 500 annual average return (long-term):** ~10% nominal, ~7% inflation-adjusted

**How Bull beats it:**
1. Sector rotation: Avoiding September, reducing exposure in recession sectors = -0.5% to +3% alpha potential annually
2. Quality filters: P/E below sector, revenue growth above average = avoids underperformers
3. Technical entries: Buying at pullbacks (50-day bounce, RSI reversion) improves cost basis vs. random entry
4. Stops: Cutting -7% losers prevents the handful of blow-ups that drag down full-year returns

**Realistic expectation:** Disciplined sector rotation strategies have outperformed buy-and-hold by an average of 2.8% annually over 30 years (per research). That's the target — not 2x the S&P, just a consistent 2–4% alpha.

---

## SECTION 9 — SESSION WORKFLOW

1. Check portfolio.md — confirm positions, cash available
2. Check VIX — determine mode (offense/caution/defense)
3. Identify economic cycle phase — confirm sector rotation context
4. Check seasonal patterns — is this a favorable month?
5. Scan watchlist — any fundamentals/technical setups triggering?
6. For each potential trade: run fundamentals checklist → confirm technical setup → size the position
7. Log in research-log.md before executing
8. Set entry, stop (-7%), and profit target at order time
9. After any trade: update portfolio.md

---

*Sources: Fidelity Sector Rotation Framework, Bespoke Investment Group, Seasonality360.com, QuantifiedStrategies.com, Journal of Financial Markets, InsideArbitrage academic research index, Lakonishok & Lee (2001), CBOE VIX data*
