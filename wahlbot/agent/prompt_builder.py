from wahlbot.polls.aggregator import PollSnapshot
from wahlbot.scanner.market_parser import Market


def build_research_prompt(market: Market, poll: PollSnapshot, historical_base_rate: float) -> str:
    return (
        "Analyze election threshold trade candidate.\n"
        f"Market: {market.title}\n"
        f"Platform: {market.platform}\n"
        f"Market implied probability: {market.market_probability:.2%}\n"
        f"Poll: {poll.latest_poll_pct:.1f}% ({poll.poll_trend}) by {poll.institute} on {poll.poll_date.isoformat()}\n"
        f"Historical base rate: {historical_base_rate:.1%}\n"
        "Return strict JSON with recommendation, confidence, adjusted_probability, reasoning, key_factors, sources."
    )
