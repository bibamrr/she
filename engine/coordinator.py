"""Master coordinator: 75% majority, risk veto, approved trades only."""

from __future__ import annotations

from typing import Any, List, Optional

from pydantic import BaseModel, Field

BUY = "BUY"
SELL = "SELL"
WAIT = "WAIT"

RISK_AGENT = "Risk_Management"
REQUIRED_MAJORITY = 0.75
MIN_SIDE_CONFIDENCE = 0.7
RISK_VETO_CONFIDENCE = 0.8
# Most sub-agents answer WAIT whenever their own signal is quiet, so counting
# abstentions as opposition made the 75% majority unreachable. Consensus is
# measured among the agents that actually took a side, and this quorum keeps a
# single lone voice from carrying a trade on its own.
MIN_DIRECTIONAL_VOTES = 3

DISPLAY_NAMES = {
    "radar_agent": "Radar",
    "quant_agent": "Quant",
    "pattern_agent": "Patterns",
    "liquidity_agent": "Liquidity",
    "news_sentiment_agent": "News_Sentiment",
    "risk_management_agent": "Risk_Management",
    "market_sentiment_agent": "Market_Sentiment",
    "on_chain_agent": "On_Chain",
}

SUB_AGENTS = (
    "Radar",
    "Quant",
    "Patterns",
    "Liquidity",
    "News_Sentiment",
    "Risk_Management",
    "Market_Sentiment",
    "On_Chain",
)


class AnalysisResult(BaseModel):
    agent_name: str
    vote: str = Field(..., description="BUY, SELL, or WAIT")
    confidence: float = Field(..., ge=0.0, le=1.0)
    reasoning: str


class MasterCoordinator:
    def __init__(self, required_majority: float = REQUIRED_MAJORITY):
        self.required_majority = required_majority
        self.sub_agents = list(SUB_AGENTS)

    def evaluate_swarm(self, results: List[AnalysisResult]) -> dict[str, Any]:
        risk_agent = next((row for row in results if _is_risk(row.agent_name)), None)
        if (
            risk_agent
            and _norm_vote(risk_agent.vote) == WAIT
            and float(risk_agent.confidence) > RISK_VETO_CONFIDENCE
        ):
            return {
                "status": "REJECTED",
                "reason": "Risk Management vetoed the trade.",
                "final_decision": WAIT,
                "consensus_ratio": 0.0,
                "average_confidence": round(float(risk_agent.confidence), 2),
                "buy_votes": 0,
                "sell_votes": 0,
            }

        buy_votes = sum(1 for row in results if _norm_vote(row.vote) == BUY)
        sell_votes = sum(1 for row in results if _norm_vote(row.vote) == SELL)
        directional = buy_votes + sell_votes
        max_votes = max(buy_votes, sell_votes)
        consensus_ratio = max_votes / directional if directional > 0 else 0.0
        final_decision = BUY if buy_votes > sell_votes else SELL if sell_votes > buy_votes else WAIT
        side_conf = [float(row.confidence) for row in results if _norm_vote(row.vote) == final_decision]
        avg_confidence = sum(side_conf) / len(side_conf) if side_conf else 0.0

        if (
            directional >= MIN_DIRECTIONAL_VOTES
            and consensus_ratio >= self.required_majority
            and avg_confidence >= MIN_SIDE_CONFIDENCE
            and final_decision in {BUY, SELL}
        ):
            return {
                "status": "APPROVED",
                "final_decision": final_decision,
                "consensus_ratio": round(consensus_ratio, 2),
                "average_confidence": round(avg_confidence, 2),
                "buy_votes": buy_votes,
                "sell_votes": sell_votes,
                "directional_votes": directional,
                "abstentions": len(results) - directional,
                "message": f"Approved {final_decision} signal with strict multi-agent consensus.",
            }
        if directional < MIN_DIRECTIONAL_VOTES:
            reason = f"Only {directional} of {len(results)} agents took a side; quorum is {MIN_DIRECTIONAL_VOTES}."
        elif consensus_ratio < self.required_majority:
            reason = "Consensus threshold not met."
        else:
            reason = "Winning side is below the confidence floor."
        return {
            "status": "HOLD",
            "reason": reason,
            "final_decision": final_decision,
            "consensus_ratio": round(consensus_ratio, 2),
            "average_confidence": round(avg_confidence, 2),
            "buy_votes": buy_votes,
            "sell_votes": sell_votes,
            "directional_votes": directional,
            "abstentions": len(results) - directional,
        }


def _norm_vote(raw: Any) -> str:
    vote = str(raw or "").strip().upper()
    if vote in {"BUY", "BULLISH", "LONG"}:
        return BUY
    if vote in {"SELL", "BEARISH", "SHORT"}:
        return SELL
    return WAIT


def _is_risk(name: str) -> bool:
    return str(name or "") in {RISK_AGENT, "risk_management_agent"}


def vote_from_direction(direction: str) -> str:
    raw = str(direction or "").strip().lower()
    if raw in {"bullish", "buy", "long"}:
        return BUY
    if raw in {"bearish", "sell", "short"}:
        return SELL
    return WAIT


def direction_from_vote(vote: str) -> str:
    norm = _norm_vote(vote)
    if norm == BUY:
        return "bullish"
    if norm == SELL:
        return "bearish"
    return "neutral"


def display_name(name: str) -> str:
    raw = str(name or "")
    return DISPLAY_NAMES.get(raw, raw)


def results_from_agents(agents: list[dict[str, Any]]) -> List[AnalysisResult]:
    rows: List[AnalysisResult] = []
    for item in agents or []:
        name = display_name(str(item.get("agent_name") or item.get("name") or "agent"))
        vote = _norm_vote(item.get("vote") or vote_from_direction(str(item.get("direction") or "")))
        try:
            confidence = max(0.0, min(1.0, float(item.get("confidence") or 0)))
        except (TypeError, ValueError):
            confidence = 0.0
        rows.append(
            AnalysisResult(
                agent_name=name,
                vote=vote,
                confidence=confidence,
                reasoning=str(item.get("reasoning") or ""),
            )
        )
    return rows


def wanted_vote(side: str) -> str:
    return _norm_vote(side)


def filter_ui_view(master_output: dict[str, Any]) -> Optional[dict[str, Any]]:
    """Subscriber view: approved setups only. Sub-agent rejects stay hidden."""
    if (master_output or {}).get("status") == "APPROVED":
        return master_output
    return None
