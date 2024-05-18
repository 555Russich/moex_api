from datetime import datetime, timezone
import logging

from aiohttp import ClientSession
from trading_helpers.csv_candles import _CSVCandles, Interval
from trading_helpers.schemas import CandleInterval
from trading_helpers.exceptions import (
    CSVCandlesNeedInsert,
    CSVCandlesNeedAppend,
    IncorrectFirstCandle,
    UnexpectedCandleInterval,
)
from aiomoex.candles import get_board_candle_borders
from aiomoex.constants import (
    Boards,
    Markets,
    Engines,
    DEFAULT_BOARD,
    DEFAULT_MARKET,
    DEFAULT_ENGINE
)
from aiomoex.constants import CandleInterval as MoexCandleInterval

from config import DIR_CANDLES  # noqa
from moex_api.schemas import Candle, Candles
from moex_api.candles import get_candles
from moex_api.date_utils import TZ_MSC


class CSVCandles(_CSVCandles):
    CANDLE = Candle
    CANDLES = Candles
    COLUMNS = {
        'open': float,
        'close': float,
        'high': float,
        'low': float,
        'value': float,
        'volume': int,
        'dt': datetime.fromisoformat,
    }
    DIR_API = DIR_CANDLES / 'moex'
    DIR_API.mkdir(exist_ok=True)

    @classmethod
    def convert_candle_interval(cls, interval: Interval) -> CandleInterval:
        match interval:
            case MoexCandleInterval.MIN_1:
                i = CandleInterval.MIN_1
            case MoexCandleInterval.MIN_10:
                i = CandleInterval.MIN_10
            case MoexCandleInterval.HOUR:
                i = CandleInterval.HOUR
            case MoexCandleInterval.DAY:
                i = CandleInterval.DAY
            case MoexCandleInterval.WEEK:
                i = CandleInterval.WEEK
            case MoexCandleInterval.MONTH:
                i = CandleInterval.MONTH
            case _:
                raise UnexpectedCandleInterval(str(interval))
        return i

    @classmethod
    async def download_or_read(
            cls,
            session: ClientSession,
            ticker: str,
            from_: datetime,
            to: datetime,
            interval: Interval,
            board: Boards = DEFAULT_BOARD,
            market: Markets = DEFAULT_MARKET,
            engine: Engines = DEFAULT_ENGINE,
    ) -> Candles:
        candles = None
        instrument_id = f'{ticker}_{board}_{market}_{engine}'
        csv = cls(instrument_id=instrument_id, interval=interval)

        from_, to = await cls.configure_datetime_range(
            session=session, ticker=ticker, from_=from_, to=to, interval=interval,
            board=board, market=market, engine=engine
        )

        if not csv.filepath.exists():
            logging.debug(f'File not exists | {instrument_id=}')
            await csv._prepare_new()
            candles = await get_candles(session=session, ticker=ticker, from_=from_, to=to, interval=interval,
                                        board=board, market=market, engine=engine)
            await csv._append(candles)
            return candles

        for retry in range(1, 4):
            try:
                return await csv._read(from_=from_, to=to, interval=csv.interval)
            except CSVCandlesNeedAppend as ex:
                logging.debug(f'Need append | {retry=} | {instrument_id=} | from_temp={ex.from_temp} | to={to}')
                # 1st candle in response is last candle in file
                candles = (await get_candles(session=session, ticker=ticker, from_=ex.from_temp, to=to,
                                             interval=interval, board=board, market=market, engine=engine))[1:]

                if candles:
                    await csv._append(candles)
                else:
                    to = ex.candles[-1].dt if to > ex.candles[-1].dt else to
            except CSVCandlesNeedInsert as ex:
                logging.debug(f'Need insert | {retry=} | {instrument_id=} | from={from_} | to_temp={ex.to_temp}')
                if retry == 3:
                    raise IncorrectFirstCandle(f'{candles[0].dt=} | {from_=}')

                candles = await get_candles(session=session, ticker=ticker, from_=from_, to=ex.to_temp,
                                            interval=interval, board=board, market=market, engine=engine)
                # 1st candle in file is last candle in get_candles response
                candles = candles[:-1]

                if candles:
                    await csv._insert(candles[:-1])
                else:
                    logging.debug(f'Nothing between from_={from_} and to_temp={ex.to_temp}')
                    from_ = ex.to_temp
            except Exception as ex:
                logging.error(f'{retry=} | {csv.filepath}', exc_info=True)
                raise ex

    @classmethod
    async def configure_datetime_range(
            cls,
            session: ClientSession,
            ticker: str,
            from_: datetime,
            to: datetime,
            interval: MoexCandleInterval,
            board: Boards = DEFAULT_BOARD,
            market: Markets = DEFAULT_MARKET,
            engine: Engines = DEFAULT_ENGINE,
    ) -> tuple[datetime, datetime]:
        r = await get_board_candle_borders(session=session, security=ticker, board=board, market=market, engine=engine)
        for d in r:
            if d['interval'] == interval:
                begin = datetime.fromisoformat(d['begin']).replace(tzinfo=TZ_MSC).astimezone(timezone.utc)
                end = datetime.fromisoformat(d['end']).replace(tzinfo=TZ_MSC).astimezone(timezone.utc)
                from_ = begin if from_ < begin else from_
                to = end if to > end else to
                break
        else:
            raise UnexpectedCandleInterval(f'{interval} | {r=}')
        return from_, to
