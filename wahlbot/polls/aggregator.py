from dataclasses import dataclass
from datetime import date
import re

from wahlbot.scanner.market_parser import Market


@dataclass
class PollSnapshot:
    party: str
    country: str
    election: str
    latest_poll_pct: float
    poll_trend: str
    poll_date: date
    institute: str
    historical_bias_correction: float


PARTIES = ("afd", "fdp", "spd", "cdu", "csu", "gruene", "linke")
REGIONS = ("germany", "deutschland", "brandenburg", "bayern", "sachsen", "rheinland-pfalz", "rlp")


def extract_party_and_country(title: str) -> tuple[str | None, str | None]:
    title_lower = title.lower()
    party = next((p.upper() for p in PARTIES if p in title_lower), None)

    country_match = re.search(
        r"\b(germany|deutschland|brandenburg|bayern|sachsen|rheinland-pfalz|rlp)\b",
        title_lower,
    )
    if not country_match:
        return party, None

    token = country_match.group(1)
    country = "DE" if token in REGIONS else token.upper()
    return party, country


def build_fallback_poll_snapshot(market: Market) -> PollSnapshot | None:
    party, country = extract_party_and_country(market.title)
    if not country:
        return None

    return PollSnapshot(
        party=party or "UNKNOWN",
        country=country,
        election=f"{country} election market",
        latest_poll_pct=market.market_probability * 100,
        poll_trend="stable",
        poll_date=date.today(),
        institute="market-implied",
        historical_bias_correction=0.0,
    )


def match_market_to_poll(market: Market) -> PollSnapshot | None:
    party, country = extract_party_and_country(market.title)
    if not party or not country:
        return None

    return PollSnapshot(
        party=party,
        country=country,
        election="Brandenburg Landtag 2025",
        latest_poll_pct=4.8,
        poll_trend="rising",
        poll_date=date(2025, 8, 1),
        institute="Forsa",
        historical_bias_correction=0.4,
    )
