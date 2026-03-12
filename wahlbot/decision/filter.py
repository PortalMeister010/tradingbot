from math import erf

from wahlbot.polls.aggregator import PollSnapshot


def historical_base_rate(poll_pct: float, sigma: float = 1.8) -> float:
    z = (5.0 - poll_pct) / (sigma * (2 ** 0.5))
    return 0.5 * (1 - erf(z))


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

    if close_race_research_enabled and is_close_race_market(market_probability, close_race_band_pct):
        return True, market_probability

    if not (poll_window_min_pct <= poll.latest_poll_pct <= poll_window_max_pct):
        return False, 0.0

    base_rate = historical_base_rate(poll.latest_poll_pct)

    trend_factor = 0.0
    if poll.poll_trend.lower() == "rising":
        trend_factor = 0.03
    elif poll.poll_trend.lower() == "falling":
        trend_factor = -0.03

    base_rate += trend_factor

    edge_pct = abs(market_probability - base_rate) * 100
    return edge_pct > min_edge_pct, base_rate
