from dataclasses import dataclass

from wahlbot.decision.engine import TradeProposal


@dataclass
class ExecutionResult:
    status: str
    attempts: int
    fill_price_cents: int | None


class OrderExecutor:
    def execute(self, proposal: TradeProposal, max_attempts: int = 3) -> ExecutionResult:
        # Placeholder behavior: immediate fill at limit.
        _ = max_attempts
        return ExecutionResult(status="filled", attempts=1, fill_price_cents=proposal.limit_price_cents)
