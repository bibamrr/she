"""
core/data_feed/ccxt_feed.py

Concrete `BaseFeed` implementation for crypto exchanges via `ccxt.pro`
(ccxt's async WebSocket layer). Targets Binance by default but is written
against ccxt's unified API, so pointing it at another supported exchange is
a one-line change in `config/settings.py` plus whatever credentials that
exchange needs.

Responsibilities of this module, precisely scoped:
    - Maintain one ccxt.pro exchange client.
    - Run three concurrent WebSocket subscription loops per symbol:
        1. `watch_trades`      -> TickEvent
        2. `watch_ohlcv`       -> OHLCVEvent (per configured timeframe)
        3. `watch_order_book`  -> OrderBookEvent
    - Normalize every message into our Pydantic schemas before publishing.
    - Publish onto the Redis event bus (injected, not hardcoded — see
      `publish_fn` in `__init__`) so this class stays testable without a
      live Redis instance.

Robustness features specifically requested:
    - Per-symbol, per-stream tasks: one bad symbol/stream doesn't take down
      every other subscription (isolated failure domains).
    - Exponential backoff is inherited from `BaseFeed`, but this class also
      applies a small per-task retry so a single symbol's `watch_trades`
      hiccup doesn't force a full exchange reconnect.
    - Explicit handling of `NetworkError` vs `ExchangeError` vs unexpected
      exceptions, since ccxt.pro raises typed exceptions for a reason.
    - Graceful `close()` of the underlying ccxt.pro client on shutdown to
      avoid leaking aiohttp sessions (a very common ccxt.pro footgun).
"""

from __future__ import annotations

import asyncio
import logging
from typing import Union, Awaitable, Callable

import ccxt.pro as ccxtpro
from ccxt.base.errors import ExchangeError, NetworkError

from core.data_feed.base_feed import BaseFeed, FeedStatus
from core.event_bus.schemas import OHLCVEvent, OrderBookEvent, OrderBookLevel, TickEvent

logger = logging.getLogger(__name__)

# Type alias for the injected publish callback: given an event, publish it
# somewhere (Redis channel, in-memory queue, etc.) and await completion.
PublishFn = Callable[[Union[TickEvent, OHLCVEvent, OrderBookEvent]], Awaitable[None]]


class CCXTFeed(BaseFeed):
    """
    Async WebSocket market data feed backed by `ccxt.pro`.

    Parameters
    ----------
    exchange_id:
        ccxt exchange identifier, e.g. "binance".
    symbols:
        Unified symbols to subscribe to, e.g. ["BTC/USDT", "ETH/USDT"].
    publish_fn:
        Async callable invoked with each normalized event. In production
        this will be `RedisEventBus.publish`; in tests it can be a simple
        list-appending stub. Injecting this keeps `CCXTFeed` decoupled from
        the concrete transport (Dependency Inversion again).
    timeframes:
        Candle timeframes to subscribe to via `watch_ohlcv`.
    api_key / api_secret:
        Exchange credentials. Only required for private data (not needed
        for public trades/OHLCV/order book, but harmless to pass through
        so this class is ready for authenticated streams later).
    sandbox:
        If True, points the exchange client at its testnet/sandbox API.
    orderbook_depth:
        Number of price levels per side to keep/publish from the order book.
    per_stream_retry_limit:
        How many consecutive failures a single (symbol, stream) task
        tolerates before it gives up and lets the outer `BaseFeed` reconnect
        loop handle a full reconnect.
    """

    def __init__(
        self,
        exchange_id: str,
        symbols: list[str],
        publish_fn: PublishFn,
        timeframes: list[str] | None = None,
        api_key: str | None = None,
        api_secret: str | None = None,
        sandbox: bool = True,
        orderbook_depth: int = 20,
        per_stream_retry_limit: int = 5,
    ) -> None:
        super().__init__(symbols=symbols, timeframes=timeframes)
        self._exchange_id = exchange_id
        self._publish_fn = publish_fn
        self._api_key = api_key
        self._api_secret = api_secret
        self._sandbox = sandbox
        self._orderbook_depth = orderbook_depth
        self._per_stream_retry_limit = per_stream_retry_limit
        self._exchange: ccxtpro.Exchange | None = None

    @property
    def name(self) -> str:
        return f"{self._exchange_id}-ccxt"

    # ------------------------------------------------------------------
    # BaseFeed contract
    # ------------------------------------------------------------------

    async def _connect_and_stream(self) -> None:
        """
        Build the ccxt.pro exchange client and run one subscription task per
        (symbol, stream-type) pair concurrently until stopped.

        Design note: we fan out into many small `asyncio.Task`s instead of
        one giant loop so a persistent failure in, say, ETH/USDT's order
        book stream cannot silently stop BTC/USDT's trade stream. Each task
        manages its own bounded retry via `_run_stream_with_retry`.
        """
        self._exchange = self._build_exchange_client()
        self._status = FeedStatus.CONNECTED

        tasks: list[asyncio.Task] = []
        try:
            for symbol in self.symbols:
                tasks.append(
                    asyncio.create_task(
                        self._run_stream_with_retry(
                            stream_name=f"trades:{symbol}",
                            stream_coro_factory=lambda s=symbol: self._watch_trades_loop(s),
                        )
                    )
                )
                tasks.append(
                    asyncio.create_task(
                        self._run_stream_with_retry(
                            stream_name=f"orderbook:{symbol}",
                            stream_coro_factory=lambda s=symbol: self._watch_orderbook_loop(s),
                        )
                    )
                )
                for tf in self.timeframes:
                    tasks.append(
                        asyncio.create_task(
                            self._run_stream_with_retry(
                                stream_name=f"ohlcv:{symbol}:{tf}",
                                stream_coro_factory=lambda s=symbol, t=tf: self._watch_ohlcv_loop(
                                    s, t
                                ),
                            )
                        )
                    )

            # Wait until either the stop event fires or every stream task has
            # given up (exhausted its retry budget) — whichever comes first.
            stop_waiter = asyncio.create_task(self._stop_event.wait())
            done, pending = await asyncio.wait(
                [stop_waiter, *tasks], return_when=asyncio.FIRST_COMPLETED
            )

            if stop_waiter in done:
                logger.info("%s: stop requested, cancelling stream tasks.", self.name)
            else:
                logger.error(
                    "%s: a stream task exhausted its retry budget; forcing full reconnect.",
                    self.name,
                )

            for task in tasks:
                if not task.done():
                    task.cancel()
            await asyncio.gather(*tasks, return_exceptions=True)
            if not stop_waiter.done():
                stop_waiter.cancel()

            if stop_waiter not in done:
                # A stream gave up permanently — raise so BaseFeed's outer
                # reconnect-with-backoff loop rebuilds the whole exchange
                # client from scratch (handles token/session-level rot).
                raise RuntimeError(f"{self.name}: stream task budget exhausted.")

        finally:
            await self._close_exchange()

    async def _emit_tick(self, event: TickEvent) -> None:
        await self._publish_fn(event)

    async def _emit_ohlcv(self, event: OHLCVEvent) -> None:
        await self._publish_fn(event)

    async def _emit_orderbook(self, event: OrderBookEvent) -> None:
        await self._publish_fn(event)

    # ------------------------------------------------------------------
    # Exchange client lifecycle
    # ------------------------------------------------------------------

    def _build_exchange_client(self) -> ccxtpro.Exchange:
        exchange_class = getattr(ccxtpro, self._exchange_id)
        client: ccxtpro.Exchange = exchange_class(
            {
                "apiKey": self._api_key,
                "secret": self._api_secret,
                "enableRateLimit": True,
                "newUpdates": True,  # watch_* returns only the newest update, not full history
            }
        )
        if self._sandbox:
            try:
                client.set_sandbox_mode(True)
            except Exception:  # noqa: BLE001
                logger.warning(
                    "%s: exchange does not support sandbox mode; using live endpoints "
                    "with the provided (hopefully read-only or testnet) credentials.",
                    self.name,
                )
        return client

    async def _close_exchange(self) -> None:
        if self._exchange is not None:
            try:
                await self._exchange.close()
            except Exception:  # noqa: BLE001
                logger.exception("%s: error while closing exchange client.", self.name)
            finally:
                self._exchange = None

    # ------------------------------------------------------------------
    # Per-stream retry wrapper
    # ------------------------------------------------------------------

    async def _run_stream_with_retry(
        self,
        stream_name: str,
        stream_coro_factory: Callable[[], Awaitable[None]],
    ) -> None:
        """
        Run a single (symbol, stream-type) loop, retrying with a short
        linear backoff on transient network errors, up to
        `self._per_stream_retry_limit` consecutive failures.

        A clean return (stop event triggered) exits silently. Exhausting the
        retry budget lets this task finish, which `_connect_and_stream`
        detects and escalates to a full reconnect.
        """
        consecutive_failures = 0
        while not self._stop_event.is_set():
            try:
                await stream_coro_factory()
                return  # stream coroutine returned cleanly -> stop was requested
            except asyncio.CancelledError:
                raise
            except NetworkError as exc:
                consecutive_failures += 1
                logger.warning(
                    "%s: network error (%d/%d): %s",
                    stream_name,
                    consecutive_failures,
                    self._per_stream_retry_limit,
                    exc,
                )
            except ExchangeError as exc:
                # Exchange-level errors (bad symbol, rate limit ban, etc.) are
                # less likely to self-resolve quickly, but we still retry a
                # bounded number of times rather than killing the whole feed.
                consecutive_failures += 1
                logger.error(
                    "%s: exchange error (%d/%d): %s",
                    stream_name,
                    consecutive_failures,
                    self._per_stream_retry_limit,
                    exc,
                )
            except Exception:  # noqa: BLE001
                consecutive_failures += 1
                logger.exception(
                    "%s: unexpected error (%d/%d).",
                    stream_name,
                    consecutive_failures,
                    self._per_stream_retry_limit,
                )

            if consecutive_failures >= self._per_stream_retry_limit:
                logger.error(
                    "%s: retry budget exhausted after %d consecutive failures.",
                    stream_name,
                    consecutive_failures,
                )
                return

            await asyncio.sleep(min(2.0 * consecutive_failures, 15.0))

    # ------------------------------------------------------------------
    # Individual stream loops
    # ------------------------------------------------------------------

    async def _watch_trades_loop(self, symbol: str) -> None:
        assert self._exchange is not None
        while not self._stop_event.is_set():
            trades = await self._exchange.watch_trades(symbol)
            for trade in trades:
                event = TickEvent(
                    source=self.name,
                    symbol=symbol,
                    timestamp_ms=trade["timestamp"],
                    price=float(trade["price"]),
                    amount=float(trade["amount"]),
                    side=trade.get("side"),
                )
                await self._emit_tick(event)

    async def _watch_ohlcv_loop(self, symbol: str, timeframe: str) -> None:
        assert self._exchange is not None
        while not self._stop_event.is_set():
            candles = await self._exchange.watch_ohlcv(symbol, timeframe)
            for candle in candles:
                ts, o, h, l, c, v = candle  # ccxt OHLCV tuple format
                event = OHLCVEvent(
                    source=self.name,
                    symbol=symbol,
                    timeframe=timeframe,
                    timestamp_ms=int(ts),
                    open=float(o),
                    high=float(h),
                    low=float(l),
                    close=float(c),
                    volume=float(v),
                    # ccxt.pro's watch_ohlcv streams the currently-forming
                    # bar repeatedly; we cannot know it is "closed" until the
                    # next bar's timestamp arrives, so downstream consumers
                    # (candle_aggregator) are responsible for that decision.
                    is_closed=False,
                )
                await self._emit_ohlcv(event)

    async def _watch_orderbook_loop(self, symbol: str) -> None:
        assert self._exchange is not None
        while not self._stop_event.is_set():
            book = await self._exchange.watch_order_book(symbol, limit=self._orderbook_depth)
            event = OrderBookEvent(
                source=self.name,
                symbol=symbol,
                timestamp_ms=book["timestamp"] or 0,
                bids=[
                    OrderBookLevel(price=float(p), amount=float(a))
                    for p, a in book["bids"][: self._orderbook_depth]
                ],
                asks=[
                    OrderBookLevel(price=float(p), amount=float(a))
                    for p, a in book["asks"][: self._orderbook_depth]
                ],
            )
            await self._emit_orderbook(event)
