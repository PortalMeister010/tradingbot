from dataclasses import dataclass

from wahlbot.agent.response_parser import AgentRecommendation
from wahlbot.config import Config
from wahlbot.decision.ev_calculator import expected_value_yes, kelly_fraction
from wahlbot.scanner.market_parser import Market


@dataclass
class TradeProposal:
    action: str
    market_id: str
    suggested_stake_usd: float
    contracts: int
    limit_price_cents: int
    ev: float
    kelly_fraction: float


def build_trade_proposal(
    market: Market,
    agent_result: AgentRecommendation,
    bankroll_usd: float,
    config: Config,
) -> TradeProposal | None:
    p_yes = agent_result.adjusted_probability
    ev_yes = expected_value_yes(p_yes, market.yes_ask_cents)

    action = "BUY_YES"
    effective_ev = ev_yes
    effective_prob = p_yes

    if ev_yes < 0:
        # synthetically evaluate NO side by mirroring YES probability/price
        action = "BUY_NO"
        effective_prob = 1 - p_yes
        effective_ev = expected_value_yes(effective_prob, 100 - market.yes_ask_cents)

    if effective_ev < config.min_ev:
        return None

    full_kelly = kelly_fraction(effective_prob, market.yes_ask_cents if action == "BUY_YES" else 100 - market.yes_ask_cents)
    position_fraction = full_kelly * config.kelly_fraction
    suggested_stake = min(config.max_stake_usd, bankroll_usd * position_fraction)
    contracts = int((suggested_stake / market.yes_ask_cents) * 100) if market.yes_ask_cents else 0

    return TradeProposal(
        action=action,
        market_id=market.market_id,
        suggested_stake_usd=round(suggested_stake, 2),
        contracts=contracts,
        limit_price_cents=market.yes_ask_cents,
        ev=round(effective_ev, 4),
        kelly_fraction=round(position_fraction, 4),
    )
