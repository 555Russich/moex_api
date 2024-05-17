from datetime import datetime
from dataclasses import dataclass
from pathlib import Path

from aiomoex.constants import CandleInterval as MoexCandleInterval


@dataclass(frozen=True)
class InstrumentInfo:
    ticker: str
    uid: str
    class_code: str
    exchange: str
    first_1day_candle_date: datetime | None = None


@dataclass(frozen=True)
class CandlesTestCase:
    filepath: Path
    dt_from: datetime
    dt_to: datetime
    count_candles: int
    dt_first_candle: datetime
    dt_last_candle: datetime
    interval: MoexCandleInterval
