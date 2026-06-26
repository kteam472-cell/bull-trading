from engine import config, pipeline
from engine.alpaca_client import RealAlpacaClient
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def main():
    client = RealAlpacaClient(config.alpaca_creds())
    risk = config.load_risk(); wl = config.load_watchlist()
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    flag = ROOT / "HALT"; log = ROOT / "logs" / "decisions.jsonl"
    log.parent.mkdir(exist_ok=True)
    vix = 15.0  # Phase 1: safe default; wire a real VIX feed in Phase 2
    out = pipeline.run(client, wl, risk, flag, log, vix=vix, today=today)
    print(f"Bull run {today}: placed={len(out['placed'])} "
          f"skipped={len(out['skipped'])} halted={out['halted']}")

if __name__ == "__main__":
    main()
