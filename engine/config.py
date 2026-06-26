import os
import yaml
from pathlib import Path
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")


def load_risk():
    # type: () -> dict
    with open(ROOT / "config" / "risk.yml") as f:
        return yaml.safe_load(f)


def load_watchlist():
    # type: () -> list
    with open(ROOT / "config" / "watchlist.txt") as f:
        return [ln.strip() for ln in f if ln.strip() and not ln.startswith("#")]


def alpaca_creds():
    # type: () -> dict
    return {
        "key": os.environ["ALPACA_KEY"],
        "secret": os.environ["ALPACA_SECRET"],
        "endpoint": os.environ.get("ALPACA_ENDPOINT", "https://paper-api.alpaca.markets/v2"),
    }
