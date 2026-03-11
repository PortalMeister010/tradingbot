def unrealized_pnl(contracts: int, avg_price_cents: int, mark_price_cents: int) -> float:
    return contracts * (mark_price_cents - avg_price_cents) / 100
