from dataclasses import dataclass
from datetime import date


@dataclass
class Market:
    market_id: str
    title: str
    platform: str
    market_probability: float
    yes_ask_cents: int
    volume_usd: float
    resolution_date: date


@dataclass
class ScannerFilters:
    market_prob_min: float
    market_prob_max: float
    min_volume_usd: float
    resolution_min_days: int
    resolution_max_days: int
    keywords: tuple[str, ...]


def is_relevant_market(market: Market, filters: ScannerFilters, today: date) -> bool:
    title_lower = market.title.lower()
    if not any(keyword in title_lower for keyword in filters.keywords):
        return False
    if not (filters.market_prob_min <= market.market_probability <= filters.market_prob_max):
        return False
    if market.volume_usd < filters.min_volume_usd:
        return False

    days_to_resolution = (market.resolution_date - today).days
    return filters.resolution_min_days <= days_to_resolution <= filters.resolution_max_days
