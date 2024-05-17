from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Self

from trading_helpers.schemas import _Candle, _Candles

from moex_api.date_utils import TZ_MSC


@dataclass(frozen=True)
class Candle(_Candle):
    value: float
    
    @classmethod
    def from_dict(cls, d: dict[str, float | int | str | datetime]) -> Self:
        return cls(
            open=d['open'],
            high=d['high'],
            low=d['low'],
            close=d['close'],
            value=d['value'],
            volume=d['volume'],
            dt=datetime.fromisoformat(d['begin']).replace(tzinfo=TZ_MSC).astimezone(timezone.utc)
        )


class Candles(_Candles):
    @classmethod
    def from_api(cls, candles: list[dict[str, float | int | str | datetime]]) -> Self:
        return cls([Candle.from_dict(d) for d in candles])
