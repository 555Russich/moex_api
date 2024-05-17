from datetime import datetime

from aiohttp import ClientSession
from aiomoex.candles import get_board_candles
from aiomoex.constants import CandleInterval as MoexCandleInterval
from aiomoex.constants import (
    Boards,
    Markets,
    Engines,
    DEFAULT_BOARD,
    DEFAULT_MARKET,
    DEFAULT_ENGINE
)

from moex_api.schemas import Candles
from moex_api.date_utils import TZ_MSC


async def get_candles(
        session: ClientSession,
        ticker: str,
        from_: datetime,
        to: datetime,
        interval: MoexCandleInterval,
        board: Boards = DEFAULT_BOARD,
        market: Markets = DEFAULT_MARKET,
        engine: Engines = DEFAULT_ENGINE,
) -> Candles:
    candles_raw = await get_board_candles(
        session=session,
        security=ticker,
        start=from_.astimezone(tz=TZ_MSC).isoformat(),
        end=to.astimezone(tz=TZ_MSC).isoformat(),
        interval=interval,
        board=board,
        market=market,
        engine=engine
    )
    return Candles.from_api(candles_raw)
