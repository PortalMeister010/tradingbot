import json
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path

from wahlbot.agent.response_parser import AgentRecommendation
from wahlbot.decision.engine import TradeProposal
from wahlbot.execution.order_executor import ExecutionResult
from wahlbot.scanner.market_parser import Market


class TradeLogger:
    def __init__(self, path: str = "trade_log.jsonl") -> None:
        self.path = Path(path)

    def append(self, trade_id: str, market: Market, proposal: TradeProposal, agent: AgentRecommendation, result: ExecutionResult) -> None:
        payload = {
            "trade_id": trade_id,
            "timestamp": datetime.now(tz=timezone.utc).isoformat(),
            "market": asdict(market),
            "proposal": asdict(proposal),
            "agent": asdict(agent),
            "execution": asdict(result),
        }
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(payload, default=str) + "\n")
