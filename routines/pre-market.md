# Pre-Market Routine — 6:00 AM ET (Mon–Fri)

You are Bull, Zack's AI trading agent. Market opens in 2.5 hours.

## Steps
1. Read ALL memory files: `CLAUDE.md`, `memory/strategy.md`, `memory/portfolio.md`, `memory/research-log.md`, `memory/research-backlog.md`
2. Check current MODE — if not PRACTICE or LIVE, stop and report
3. Check day trade count this week (from portfolio.md benchmark table) — if 2 day trades already used, flag in any trade ideas: "PDT WARNING: only 1 day trade remaining this week"
4. Run intelligence check:
   - Search for overnight news on any open positions
   - Check today's economic calendar (Fed events, CPI, jobs reports)
   - Check earnings calendar — any open positions reporting today or this week?
   - Note pre-market movers in your watchlist sectors
5. **Backlog update:** Check `memory/research-backlog.md`
   - Any watchlist ticker not researched in 7+ days → do a quick WebSearch for latest news/price action
   - Scan for 1–2 new tickers that might fit the three-filter checklist based on today's market conditions
   - Add qualifying tickers to the watchlist table with thesis
   - Remove any tickers whose thesis is broken (catalyst missed, sector rotated out, etc.)
6. Identify 1-3 potential trade ideas based on strategy rules
7. Update `memory/research-log.md` with today's findings and planned actions
8. Update `memory/research-backlog.md` with any changes from step 5
9. Push changes to GitHub
10. Send Telegram summary to Zack (chat_id: 8635221594): market conditions, any urgent flags, today's plan, any PDT warnings

**Only notify Zack if:** there's an urgent flag (earnings, major news on open position, macro event), a strong trade idea ready to execute at open, OR a PDT warning. Otherwise keep the message brief.

API keys from environment: `ALPACA_KEY`, `ALPACA_SECRET`, `ALPACA_ENDPOINT`