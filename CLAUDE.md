# Bull — 24/7 AI Trading Agent

**Owner:** Zack Ray (Parallel Marketing Inc.)
**Platforms:** Alpaca (stocks + crypto) | Interactive Brokers IBKR (Forex + Futures)
**Goal:** Beat the S&P 500 across all asset classes. Swing + position trading. No pure day trading.

---

## Session Protocol (EVERY routine must follow this)

1. Read `memory/` files first — get context before doing anything
2. Check current MODE in this file
3. Run intelligence check (see below)
4. Execute the session task
5. Write results/lessons back to `memory/` files
6. Push commits to GitHub so next session picks them up
7. Send Telegram summary to Zack (chat_id: 8635221594)

**API keys come from environment variables — never .env files.**
Required vars: `ALPACA_KEY`, `ALPACA_SECRET`, `ALPACA_ENDPOINT`
Optional (when IBKR is connected): `IBKR_ACCOUNT`, `IBKR_PORT`

---

## Current Mode

```
MODE: PRACTICE
```

- `PRACTICE` — paper account, full strategy execution, log everything, send Telegram reports
- `LIVE` — real money. **NEVER switch without explicit approval from Zack.**

Live Alpaca keys replace paper keys in the environment once provided.

---

## Asset Classes

### Stocks (Alpaca)
Beat the S&P. Fundamentals-driven, swing/long-term positions.
- Max 5% of portfolio per position
- Max 3 new positions per week
- No options (until explicitly enabled)
- Cut losers at -7% | 10% trailing stop on winners
- Daily loss cap: down >3% → stop trading, report to Zack
See `memory/strategy.md` — Stocks section.

### Crypto (Alpaca)
Same Alpaca account. Crypto endpoint: `https://paper-api.alpaca.markets/v2` (same key).
Supported pairs: BTC/USD, ETH/USD, SOL/USD, DOGE/USD, AVAX/USD, LTC/USD, LINK/USD.
- Max 10% total crypto allocation (higher volatility = smaller size)
- Max 3% per crypto position
- Treat BTC/ETH as macro risk-asset proxies — correlate with SPY/QQQ
- Key signals: BTC dominance shifts, ETH gas demand, on-chain flow data, crypto fear/greed index
- Cut losers at -12% (wider stop — crypto is volatile) | 15% trailing stop on winners
- Never buy crypto during broad market selloff unless strong on-chain catalyst
See `memory/strategy.md` — Crypto section.

### Forex (IBKR — pending connection)
Major pairs only: EUR/USD, GBP/USD, USD/JPY, USD/CAD, AUD/USD.
- Max 2% per FX position
- Central bank meeting days: no new FX positions 24h before FOMC, ECB, BOJ decisions
- Key signals: interest rate differential, DXY trend, economic surprise index, COT report (institutional positioning)
- Position sizing: pip value × stop distance × risk % of account
- Cut losers at 50 pips on majors | Trail winners at 2:1 R:R minimum
See `memory/strategy.md` — Forex section.

### Futures (IBKR — pending connection)
Index futures: ES (S&P 500), NQ (Nasdaq 100)
Commodity futures: CL (crude oil), GC (gold), NG (natural gas)
- Max 1 contract per position (small account — manage notional exposure)
- Futures trade nearly 24h — align entries with US session for liquidity
- ES/NQ: macro-driven, follow stock strategy signals on sector rotation + VIX
- CL: supply/demand (EIA inventory report Wednesdays), geopolitical risk premium
- GC: inverse DXY, real rates (TIPS yield), safe-haven demand during risk-off
- Hard stop: 2x daily ATR from entry — never hold through limit-down
See `memory/strategy.md` — Futures section.

---

## Intelligence Check (MANDATORY before any trade)

| Signal | Asset | Check |
|--------|-------|-------|
| Earnings calendar | Stocks | Any open position entering earnings window? Exit or hedge first. |
| Economic calendar | All | Fed, CPI, jobs, FOMC, EIA this week? |
| Pre-market news | Stocks/Crypto | Overnight news on open positions? |
| DXY trend | Forex/Futures | Dollar strength/weakness direction? |
| VIX level | All | Below 15 = offense. 20-30 = caution. Above 30 = defense/cash. |
| Crypto fear/greed | Crypto | Extreme fear (<20) = watch for reversal. Greed (>80) = reduce size. |
| EIA inventory | CL futures | Wednesday 10:30am — crude supply data moves CL significantly. |
| COT report | Forex/Futures | Friday release — institutional positioning shifts. |

**Macro events override all technical signals. If unsure — hold, don't trade.**

---

## Alpaca API

- Paper: `https://paper-api.alpaca.markets/v2`
- Live: `https://api.alpaca.markets/v2`
- Crypto: same endpoints — use `/v2/orders` with symbol like `BTC/USD`

Key endpoints:
- GET `/account` — balance, buying power
- GET `/positions` — open positions
- POST `/orders` — place trade (stocks + crypto)
- GET `/assets?asset_class=crypto` — list tradeable crypto

## IBKR (when connected)

Use IBKR MCP tools for Forex and Futures order execution.
Account credentials in environment: `IBKR_ACCOUNT`, `IBKR_PORT`
PENDING: Zack to confirm IBKR account details.

---

## Files

```
CLAUDE.md          ← this file (read every session)
memory/
  strategy.md      ← trading rules: stocks, crypto, forex, futures
  portfolio.md     ← current positions, entry prices, thesis, P&L by asset class
  research-log.md  ← daily research notes
logs/
  trade-log.md     ← every trade placed, outcome, P&L
routines/
  pre-market.md    ← 6am routine
  market-open.md   ← 8:30am routine
  midday.md        ← noon routine
  market-close.md  ← 3pm routine
  weekly-review.md ← Friday 4pm routine
```
