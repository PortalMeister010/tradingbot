from datetime import date
from uuid import uuid4

from wahlbot.agent.perplexity import PerplexityClient
from wahlbot.agent.prompt_builder import build_research_prompt
from wahlbot.approval.telegram_bot import build_approval_message
from wahlbot.config import DEFAULT_CONFIG
from wahlbot.decision.engine import build_trade_proposal
from wahlbot.decision.filter import historical_base_rate, prefilter_candidate
from wahlbot.execution.logger import TradeLogger
from wahlbot.execution.order_executor import OrderExecutor
from wahlbot.polls.aggregator import match_market_to_poll
from wahlbot.scanner.kalshi import KalshiClient, scan_relevant_markets
from wahlbot.scanner.market_parser import ScannerFilters


def run_once(bankroll_usd: float = 1000.0) -> None:
    cfg = DEFAULT_CONFIG
    scan_filters = ScannerFilters(
        market_prob_min=cfg.market_prob_min,
        market_prob_max=cfg.market_prob_max,
        min_volume_usd=cfg.min_volume_usd,
        resolution_min_days=cfg.resolution_min_days,
        resolution_max_days=cfg.resolution_max_days,
        keywords=cfg.election_keywords,
    )

    scanner = KalshiClient()
    agent = PerplexityClient()
    executor = OrderExecutor()
    logger = TradeLogger()

    for market in scan_relevant_markets(scanner, scan_filters, today=date.today()):
        poll = match_market_to_poll(market)
        if poll is None:
            continue

        should_run_agent, base_rate = prefilter_candidate(
            poll=poll,
            market_probability=market.market_probability,
            poll_window_min_pct=cfg.poll_window_min_pct,
            poll_window_max_pct=cfg.poll_window_max_pct,
            min_edge_pct=cfg.min_edge_pct,
            has_open_position=False,
        )
        if not should_run_agent:
            continue

        prompt = build_research_prompt(market=market, poll=poll, historical_base_rate=base_rate or historical_base_rate(poll.latest_poll_pct))
        agent_result = agent.research(prompt)
        proposal = build_trade_proposal(market=market, agent_result=agent_result, bankroll_usd=bankroll_usd, config=cfg)
        if proposal is None:
            continue

        trade_id = str(uuid4())
        approval_msg = build_approval_message(trade_id, market, proposal, agent_result)
        print(approval_msg.text)

        # In production: wait for human approval. Here we simulate approval.
        result = executor.execute(proposal)
        logger.append(trade_id, market, proposal, agent_result, result)


if __name__ == "__main__":
    run_once()
