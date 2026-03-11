import json

from wahlbot.agent.response_parser import AgentRecommendation, parse_agent_response


class PerplexityClient:
    """Stub that simulates structured AI research output."""

    def research(self, prompt: str) -> AgentRecommendation:
        # Replace with API call; keep deterministic skeleton for now.
        _ = prompt
        raw = json.dumps(
            {
                "recommendation": "BUY_NO",
                "confidence": 0.72,
                "adjusted_probability": 0.38,
                "reasoning": "Poll trend and bias-adjusted base rate suggest market is overpriced.",
                "key_factors": ["Institute bias +0.6%", "Recent momentum mixed"],
                "sources": ["https://example.org"],
            }
        )
        return parse_agent_response(raw)
