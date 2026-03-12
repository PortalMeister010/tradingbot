from dataclasses import dataclass

from wahlbot.agent.response_parser import AgentRecommendation
from wahlbot.decision.engine import TradeProposal
from wahlbot.scanner.market_parser import Market


@dataclass
class ApprovalMessage:
    trade_id: str
    text: str


def build_approval_message(trade_id: str, market: Market, proposal: TradeProposal, agent: AgentRecommendation) -> ApprovalMessage:
    text = (
        "🗳️ TRADE KANDIDAT GEFUNDEN\n\n"
        f"Markt: {market.title}\n"
        f"Plattform: {market.platform}\n"
        f"Marktpreis: {market.yes_ask_cents}¢\n"
        f"Agent-Einschätzung: {agent.adjusted_probability:.0%}\n\n"
        f"📊 Empfehlung: {proposal.action}\n"
        f"💰 Vorgeschlagener Einsatz: ${proposal.suggested_stake_usd:.2f}\n"
        f"📈 Erwarteter EV: {proposal.ev:.2%}\n"
    )
    return ApprovalMessage(trade_id=trade_id, text=text)
