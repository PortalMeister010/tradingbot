from datetime import date
from typing import Iterable

from wahlbot.scanner.market_parser import Market, ScannerFilters, is_relevant_market


class KalshiClient:
    """Placeholder client. Replace with authenticated REST integration."""

    def fetch_markets(self) -> list[Market]:
        return [
            Market(
                market_id="kalshi-demo-1",
                title="Will AfD exceed 5% in Brandenburg election?",
                platform="kalshi",
                market_probability=0.61,
                yes_ask_cents=62,
                volume_usd=18400,
                resolution_date=date(2025, 9, 14),
            )
        ]


def scan_relevant_markets(client: KalshiClient, filters: ScannerFilters, today: date) -> Iterable[Market]:
    for market in client.fetch_markets():
        if is_relevant_market(market=market, filters=filters, today=today):
            yield market
