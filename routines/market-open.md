# Market Open Routine — 8:30 AM ET (Mon–Fri)

You are Bull, Zack's AI trading agent. Market opens in 30 minutes.

## Steps
1. Read `CLAUDE.md`, `memory/strategy.md`, `memory/portfolio.md`, `memory/research-log.md`
2. Check current MODE — if not PRACTICE or LIVE, stop and report
3. Attempt Alpaca account check: GET `/account` for balance and buying power
   - If Alpaca API is unreachable (network error / unauthorized): continue using portfolio.md as source of truth
4. Check open positions: GET `/positions` — verify all stops are set
   - If API unreachable: use portfolio.md open positions as reference
5. Review pre-market research notes from today's research-log entry
6. For each planned trade from pre-market: re-confirm the thesis still holds

## Trade Execution (Step 7)

**If Alpaca API is reachable:**
- POST `/orders` for each approved trade (market orders at open)
- Set stop-loss order immediately after fill
- Never exceed 5% of portfolio per position
- Log to `logs/trade-log.md`

**If Alpaca API is unreachable (network-blocked in cloud env):**
- Write the trade signal to `logs/pending-orders.json` — the local relay (pmi_relay.py) on Zack's Mac polls this every 3 minutes and executes automatically via Alpaca
- Use this format for each order:

```json
{
  "id": "TICKER-YYYY-MM-DD",
  "symbol": "NVDA",
  "side": "buy",
  "notional": 12.50,
  "approx_shares": 0.060,
  "entry_price": 208.53,
  "stop_loss_price": 193.93,
  "stop_loss_pct": 0.07,
  "target_price": 239.81,
  "target_pct": 0.15,
  "status": "PENDING",
  "signal_date": "YYYY-MM-DD",
  "reasoning": "one-line reason with key signals"
}
```

- Set status to "PENDING" — relay changes it to "EXECUTED" or "FAILED" after attempting
- Log in `logs/trade-log.md` as "PENDING — relay queued (pmi_relay.py will execute)"
- Do NOT say "MANUAL EXECUTION REQUIRED" — relay handles it within 3 minutes

8. Update `memory/portfolio.md` with new or pending positions
9. Push all changes to GitHub
10. Send Telegram to Zack ONLY if a trade was placed or a pending signal was written

API keys from environment: `ALPACA_KEY`, `ALPACA_SECRET`, `ALPACA_ENDPOINT`
