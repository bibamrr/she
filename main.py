"""
main.py

Platform Entrypoint: Spun up to launch the entire Virtual Hedge Fund engine.
"""

from __future__ import annotations

import asyncio
import logging

from config.settings import get_settings
from core.data_feed.ccxt_feed import CCXTFeed
from core.event_bus.redis_bus import RedisEventBus
from core.risk.risk_engine import RiskEngine
from oracle_hub.hub import OracleHub
from agents.radar_scout import RadarScout
from agents.visionary import VisionaryAgent
from agents.orderbook_sniper import OrderBookSniper

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger(__name__)


async def main() -> None:
    settings = get_settings()
    logger.info("Starting %s in %s mode...", settings.PROJECT_NAME, settings.environment)

    # 1. Initialize Event Bus
    event_bus = RedisEventBus.from_settings(settings)
    await event_bus.connect()

    # 2. Initialize Data Feed
    feed = CCXTFeed(
        exchange_id="binance",
        symbols=settings.default_symbols,
        publish_fn=event_bus.publish_market_data,
        timeframes=settings.default_timeframes,
        sandbox=settings.binance_testnet,
    )

    # 3. Initialize Agents & Hub
    radar = RadarScout(event_bus=event_bus, symbols=settings.default_symbols)
    visionary = VisionaryAgent(
        event_bus=event_bus,
        symbols=settings.default_symbols,
        timeframes=settings.default_timeframes,
        execution_timeframe="1m",
    )
    sniper = OrderBookSniper(event_bus=event_bus, symbols=settings.default_symbols)
    
    risk_engine = RiskEngine(settings)
    oracle_hub = OracleHub(event_bus=event_bus, risk_engine=risk_engine)

    # 4. Start everything concurrently
    await feed.start()
    await radar.start()
    await visionary.start()
    await sniper.start()

    logger.info("🚀 All systems online and monitoring markets. Press Ctrl+C to stop.")

    try:
        # Keep running indefinitely
        while True:
            await asyncio.sleep(3600)
    except (KeyboardInterrupt, asyncio.CancelledError):
        logger.info("Shutting down platform gracefully...")
    finally:
        await sniper.stop()
        await visionary.stop()
        await radar.stop()
        await feed.stop()
        await event_bus.close()
        logger.info("🛑 Platform shutdown complete.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
