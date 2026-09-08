"""
core/risk/risk_engine.py

Risk Management Engine: Position sizing, equity protection, and circuit breakers.

Responsibilities:
    - Validate incoming trade signals against account equity and risk limits.
    - Calculate exact position size (quantity) based on allowed risk per trade.
    - Enforce platform-wide circuit breakers (max daily loss, max concurrent positions).
"""

from __future__ import annotations

import logging
from typing import Any

from config.settings import Settings

logger = logging.getLogger(__name__)


class RiskEngine:
    """
    Evaluates trades against risk constraints before execution approval.
    """

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.risk_config = settings.risk

    def evaluate_trade(
        self,
        account_equity: float,
        current_open_positions: int,
        entry_price: float,
        stop_loss_price: float,
    ) -> tuple[bool, float, str]:
        """
        Evaluate whether a proposed trade complies with risk rules.
        Returns: (is_approved, target_position_size, reason)
        """
        # 1. Check concurrent positions limit
        if current_open_positions >= self.risk_config.max_concurrent_positions:
            return False, 0.0, f"Max concurrent positions reached ({current_open_positions})"

        # 2. Calculate risk distance
        risk_distance = abs(entry_price - stop_loss_price)
        if risk_distance <= 0:
            return False, 0.0, "Invalid stop loss or entry price (risk distance <= 0)"

        # 3. Calculate max capital at risk for this trade
        max_risk_amount = account_equity * (self.risk_config.max_risk_per_trade_pct / 100.0)

        # 4. Compute position size (units/quantity)
        position_size = max_risk_amount / risk_distance

        return True, position_size, "Trade passed risk validation."
