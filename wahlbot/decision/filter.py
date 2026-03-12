from wahlbot.polls.aggregator import PollSnapshot


BASE_RATE_TABLE: list[tuple[tuple[float, float], float]] = [
    ((3.0, 3.9), 0.08),
    ((4.0, 4.4), 0.18),
    ((4.5, 4.9), 0.30),
    ((5.0, 5.4), 0.62),
    ((5.5, 5.9), 0.75),
    ((6.0, 100.0), 0.87),
]


def historical_base_rate(poll_pct: float) -> float:
    for (lower, upper), rate in BASE_RATE_TABLE:
        if lower <= poll_pct <= upper:
            return rate
    return 0.0


def is_close_race_market(market_probability: float, close_race_band_pct: float) -> bool:
    distance_to_even_pct = abs(market_probability - 0.5) * 100
    return distance_to_even_pct <= close_race_band_pct


def prefilter_candidate(
    poll: PollSnapshot,
    market_probability: float,
    poll_window_min_pct: float,
    poll_window_max_pct: float,
    min_edge_pct: float,
    has_open_position: bool,
    close_race_research_enabled: bool,
    close_race_band_pct: float,
) -> tuple[bool, float]:

    if has_open_position:
        return False, 0.0

    if close_race_research_enabled and is_close_race_market(
        market_probability, close_race_band_pct
    ):
        return True, market_probability

    if not (poll_window_min_pct <= poll.latest_poll_pct <= poll_window_max_pct):
        return False, 0.0

    base_rate = historical_base_rate(poll.latest_poll_pct)
    edge_pct = abs(market_probability - base_rate) * 100
    return edge_pct > min_edge_pct, base_rate
