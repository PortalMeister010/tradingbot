from wahlbot.polls.aggregator import PollSnapshot


class DawumClient:
    """Stub for dawum.de polling data retrieval."""

    def get_latest(self, party: str, election: str) -> PollSnapshot | None:
        return None
