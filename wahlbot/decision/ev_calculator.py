def expected_value_yes(probability: float, price_cents: int) -> float:
    stake = price_cents / 100
    profit_if_yes = (100 - price_cents) / 100
    return probability * profit_if_yes - (1 - probability) * stake


def kelly_fraction(probability: float, price_cents: int) -> float:
    b = (100 - price_cents) / price_cents
    q = 1 - probability
    value = (probability * b - q) / b
    return max(0.0, value)
