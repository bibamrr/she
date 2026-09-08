from __future__ import annotations

from engine.coordinator import (
    MIN_DIRECTIONAL_VOTES,
    MasterCoordinator,
    results_from_agents,
)

COORDINATOR = MasterCoordinator()


def _agents(*votes: tuple[str, str, float]) -> list[dict]:
    return [
        {"name": name, "vote": vote, "confidence": confidence}
        for name, vote, confidence in votes
    ]


def _quiet(*names: str) -> list[tuple[str, str, float]]:
    return [(name, "WAIT", 0.3) for name in names]


def test_abstentions_do_not_block_a_clear_side() -> None:
    """Five quiet agents must not veto three that agree — the old bug."""
    agents = _agents(
        ("quant_agent", "SELL", 0.93),
        ("pattern_agent", "SELL", 0.8),
        ("market_sentiment_agent", "SELL", 0.75),
        *_quiet(
            "radar_agent",
            "liquidity_agent",
            "risk_management_agent",
            "news_sentiment_agent",
            "on_chain_agent",
        ),
    )
    verdict = COORDINATOR.evaluate_swarm(results_from_agents(agents))
    assert verdict["status"] == "APPROVED"
    assert verdict["final_decision"] == "SELL"
    assert verdict["consensus_ratio"] == 1.0
    assert verdict["directional_votes"] == 3
    assert verdict["abstentions"] == 5


def test_split_directional_vote_still_holds() -> None:
    """The real SUI case: 1 BUY vs 2 SELL is 67% — under the 75% majority."""
    agents = _agents(
        ("quant_agent", "SELL", 0.93),
        ("pattern_agent", "SELL", 0.55),
        ("news_sentiment_agent", "BUY", 0.71),
        *_quiet("radar_agent", "liquidity_agent", "risk_management_agent"),
    )
    verdict = COORDINATOR.evaluate_swarm(results_from_agents(agents))
    assert verdict["status"] == "HOLD"
    assert verdict["consensus_ratio"] == 0.67
    assert verdict["reason"] == "Consensus threshold not met."


def test_lone_voice_cannot_carry_a_trade() -> None:
    agents = _agents(
        ("quant_agent", "BUY", 0.99),
        *_quiet("radar_agent", "pattern_agent", "liquidity_agent"),
    )
    verdict = COORDINATOR.evaluate_swarm(results_from_agents(agents))
    assert verdict["status"] == "HOLD"
    assert verdict["directional_votes"] == 1
    assert str(MIN_DIRECTIONAL_VOTES) in verdict["reason"]


def test_low_confidence_side_is_held() -> None:
    agents = _agents(
        ("quant_agent", "BUY", 0.5),
        ("pattern_agent", "BUY", 0.55),
        ("on_chain_agent", "BUY", 0.6),
        *_quiet("radar_agent"),
    )
    verdict = COORDINATOR.evaluate_swarm(results_from_agents(agents))
    assert verdict["status"] == "HOLD"
    assert verdict["consensus_ratio"] == 1.0
    assert verdict["reason"] == "Winning side is below the confidence floor."


def test_risk_veto_still_wins() -> None:
    agents = _agents(
        ("quant_agent", "BUY", 0.95),
        ("pattern_agent", "BUY", 0.9),
        ("on_chain_agent", "BUY", 0.88),
        ("risk_management_agent", "WAIT", 0.91),
    )
    verdict = COORDINATOR.evaluate_swarm(results_from_agents(agents))
    assert verdict["status"] == "REJECTED"
    assert verdict["reason"] == "Risk Management vetoed the trade."
