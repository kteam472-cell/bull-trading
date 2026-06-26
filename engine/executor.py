def execute(decision, client, today):
    if not decision.get("go"):
        return None
    if decision.get("stop_price") is None:
        raise ValueError("refusing to place an order without a broker stop")
    coid = f"bull-{decision['symbol']}-{today}"
    return client.submit_bracket(
        symbol=decision["symbol"], qty=decision["qty"],
        entry_type=decision["entry_type"], stop_price=decision["stop_price"],
        take_profit=None, client_order_id=coid)
