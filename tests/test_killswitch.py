from engine import killswitch
from engine.fake_alpaca import FakeAlpacaClient

def test_halt_flattens_and_sets_flag(tmp_path):
    flag = tmp_path / "HALT"
    c = FakeAlpacaClient(positions=[{"symbol": "AAPL", "qty": "10"}])
    killswitch.halt(c, flag)
    assert c.cancelled is True
    assert c.get_positions() == []
    assert killswitch.is_halted(flag) is True

def test_clear(tmp_path):
    flag = tmp_path / "HALT"
    killswitch.halt(FakeAlpacaClient(), flag)
    killswitch.clear(flag)
    assert killswitch.is_halted(flag) is False
