from pathlib import Path
from datetime import datetime, timezone

def halt(client, flag_path):
    client.cancel_all_orders()
    client.close_all_positions()
    Path(flag_path).write_text(datetime.now(timezone.utc).isoformat())
    return {"halted": True}

def is_halted(flag_path):
    return Path(flag_path).exists()

def clear(flag_path):
    p = Path(flag_path)
    if p.exists(): p.unlink()
