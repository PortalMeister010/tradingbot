from wahlbot.polls.aggregator import PollSnapshot


class WikipediaPollScraper:
    """Stub for wikipedia poll scraping fallback."""

    def get_latest(self, party: str, election: str) -> PollSnapshot | None:
        return None
