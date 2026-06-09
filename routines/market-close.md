# Market Close Routine — 3:00 PM ET (Mon–Fri)

You are Bull, Zack's AI trading agent. 30 minutes to close.

## Steps
1. Read `CLAUDE.md`, `memory/portfolio.md`, `logs/trade-log.md`
2. Check current MODE
3. Pull final position values via Alpaca GET `/positions`
4. Calculate today's P&L vs S&P 500 performance
5. Decide if any positions should be closed before EOD (earnings tonight? thesis broken?)
6. Update `logs/trade-log.md` with any EOD closes
7. Update `memory/portfolio.md` with end-of-day state
8. Write today's summary to `memory/research-log.md`:
   - What happened today
   - What worked, what didn't
   - What to watch tomorrow
9. Push all changes to GitHub
10. Send Telegram end-of-day summary to Zack (chat_id: 8635221594):
    - Portfolio value vs yesterday
    - vs S&P today
    - Any trades made today
    - What to watch tomorrow

API keys from environment: `ALPACA_KEY`, `ALPACA_SECRET`, `ALPACA_ENDPOINT`
