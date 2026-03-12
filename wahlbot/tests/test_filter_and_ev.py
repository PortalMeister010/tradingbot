from datetime import date

from wahlbot.agent.response_parser import AgentRecommendation
from wahlbot.config import DEFAULT_CONFIG
from wahlbot.decision.engine import build_trade_proposal
from wahlbot.decision.ev_calculator import expected_value_yes
from wahlbot.decision.filter import historical_base_rate, is_close_race_market, prefilter_candidate
from wahlbot.polls.aggregator import PollSnapshot, build_fallback_poll_snapshot
from wahlbot.scanner.market_parser import Market


def test_historical_base_rate():
    assert historical_base_rate(4.8) == 0.30


def test_prefilter_candidate_edge_true():
    poll = PollSnapshot(
        party="AFD",
        country="DE",
        election="Brandenburg",
        latest_poll_pct=4.8,
        poll_trend="rising",
        poll_date=date(2025, 8, 1),
        institute="Forsa",
        historical_bias_correction=0.4,
    )
    decision, base_rate = prefilter_candidate(
        poll=poll,
        market_probability=0.61,
        poll_window_min_pct=3.0,
        poll_window_max_pct=7.0,
        min_edge_pct=10,
        has_open_position=False,
        close_race_research_enabled=True,
        close_race_band_pct=8.0,
    )
    assert decision is True
    assert base_rate == 0.30


def test_close_race_market_is_selected_for_research():
    assert is_close_race_market(0.51, close_race_band_pct=8.0) is True


def test_build_fallback_poll_snapshot_for_state_election_market():
    market = Market(
        market_id="m2",
        title="Will CDU win Rheinland-Pfalz landtagswahl?",
        platform="kalshi",
        market_probability=0.49,
        yes_ask_cents=49,
        volume_usd=10000,
        resolution_date=date(2026, 3, 1),
    )
    snapshot = build_fallback_poll_snapshot(market)
    assert snapshot is not None
    assert snapshot.country == "DE"


def test_expected_value_yes_positive():
    assert expected_value_yes(0.65, 50) > 0


def test_build_trade_proposal():
    market = Market(
        market_id="m1",
        title="Will AfD exceed 5% in Brandenburg election?",
        platform="kalshi",
        market_probability=0.61,
        yes_ask_cents=62,
        volume_usd=18400,
        resolution_date=date(2025, 9, 14),
    )
    agent = AgentRecommendation(
        recommendation="BUY_NO",
        confidence=0.7,
        adjusted_probability=0.38,
        reasoning="x",
        key_factors=[],
        sources=[],
    )
    proposal = build_trade_proposal(market, agent, bankroll_usd=1000, config=DEFAULT_CONFIG)
    assert proposal is not None
    assert proposal.suggested_stake_usd <= DEFAULT_CONFIG.max_stake_usd
