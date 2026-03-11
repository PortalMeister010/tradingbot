import json
from dataclasses import dataclass


@dataclass
class AgentRecommendation:
    recommendation: str
    confidence: float
    adjusted_probability: float
    reasoning: str
    key_factors: list[str]
    sources: list[str]


def parse_agent_response(raw_text: str) -> AgentRecommendation:
    payload = json.loads(raw_text)
    return AgentRecommendation(
        recommendation=payload["recommendation"],
        confidence=float(payload["confidence"]),
        adjusted_probability=float(payload["adjusted_probability"]),
        reasoning=payload["reasoning"],
        key_factors=list(payload.get("key_factors", [])),
        sources=list(payload.get("sources", [])),
    )
