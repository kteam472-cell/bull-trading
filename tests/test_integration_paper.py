import os, pytest
from engine import config
from engine.alpaca_client import RealAlpacaClient

pytestmark = pytest.mark.skipif(os.environ.get("RUN_INTEGRATION") != "1",
                                reason="set RUN_INTEGRATION=1 to hit Alpaca paper")

def test_real_account_reachable():
    c = RealAlpacaClient(config.alpaca_creds())
    acct = c.get_account()
    assert acct["status"] == "ACTIVE"
    assert "paper" in config.alpaca_creds()["endpoint"]   # never live
