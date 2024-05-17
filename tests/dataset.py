from datetime import datetime, timezone

from aiomoex.constants import CandleInterval as MoexCandleInterval

from tests.conftest import TEST_DIR_CANDLES
from tests.schemas import InstrumentInfo, CandlesTestCase


SBER = InstrumentInfo(
    ticker='SBER',
    uid='e6123145-9665-43e0-8413-cd61b8aa9b13',
    class_code='TQBR',
    exchange='MOEX_EVENING_WEEKEND',
    first_1day_candle_date=datetime(2000, 1, 4, 7, 0, tzinfo=timezone.utc)
)
CNTL = InstrumentInfo(
    ticker='CNTL',
    uid='c05fd0a1-0c8e-4bc3-bf9e-43e364d278ef',
    class_code='TQBR',
    exchange='MOEX'
)
POSI = InstrumentInfo(
    ticker='POSI',
    uid='de08affe-4fbd-454e-9fd1-46a81b23f870',
    class_code='TQBR',
    exchange='MOEX_EVENING_WEEKEND',
    first_1day_candle_date=datetime(2021, 12, 17, 0, 0, tzinfo=timezone.utc)
)

CASE_SBER_FULL_RANGE_EXISTS = CandlesTestCase(
    filepath=TEST_DIR_CANDLES / f'SBER_full_range_exists.csv',
    dt_from=datetime(year=2024, month=2, day=19, hour=13, minute=0, tzinfo=timezone.utc),
    dt_to=datetime(year=2024, month=2, day=22, hour=12, minute=59, tzinfo=timezone.utc),
    count_candles=2435,
    dt_first_candle=datetime(year=2024, month=2, day=19, hour=13, tzinfo=timezone.utc),
    dt_last_candle=datetime(year=2024, month=2, day=22, hour=12, minute=59, tzinfo=timezone.utc),
    interval=MoexCandleInterval.MIN_1
)

CASE_CNTL_FULL_RANGE_EXISTS = CandlesTestCase(
    filepath=TEST_DIR_CANDLES / f'CNTL_full_range_exists.csv',
    dt_from=datetime(year=2024, month=2, day=19, hour=7, minute=0, tzinfo=timezone.utc),
    dt_to=datetime(year=2024, month=2, day=22, hour=6, minute=59, tzinfo=timezone.utc),
    count_candles=811,
    dt_first_candle=datetime(year=2024, month=2, day=19, hour=7, tzinfo=timezone.utc),
    dt_last_candle=datetime(year=2024, month=2, day=22, hour=6, minute=59, tzinfo=timezone.utc),
    interval=MoexCandleInterval.MIN_1
)
CASE_CNTL_GAP_IN_THE_BEGINNING = CandlesTestCase(
    filepath=TEST_DIR_CANDLES / f'CNTL_gap_in_the_beginning.csv',
    dt_from=datetime(year=2024, month=2, day=19, hour=13, minute=0, tzinfo=timezone.utc),
    dt_to=datetime(year=2024, month=2, day=22, hour=6, minute=59, tzinfo=timezone.utc),
    count_candles=590,
    dt_first_candle=datetime(year=2024, month=2, day=19, hour=13, minute=5, tzinfo=timezone.utc),
    dt_last_candle=datetime(year=2024, month=2, day=22, hour=6, minute=59, tzinfo=timezone.utc),
    interval=MoexCandleInterval.MIN_1
)
CASE_CNTL_GAP_IN_THE_END = CandlesTestCase(
    filepath=TEST_DIR_CANDLES / 'CNTL_gap_in_the_end.csv',
    dt_from=datetime(year=2024, month=2, day=19, hour=7, minute=0, tzinfo=timezone.utc),
    dt_to=datetime(year=2024, month=2, day=19, hour=16, minute=0, tzinfo=timezone.utc),
    count_candles=266,
    dt_first_candle=datetime(year=2024, month=2, day=19, hour=7, minute=0, tzinfo=timezone.utc),
    dt_last_candle=datetime(year=2024, month=2, day=19, hour=15, minute=48, tzinfo=timezone.utc),
    interval=MoexCandleInterval.MIN_1
)
CASE_POSI_GAPS_EVERYWHERE = CandlesTestCase(
    filepath=TEST_DIR_CANDLES / 'POSI_gaps_everywhere.csv',
    dt_from=datetime(year=2019, month=5, day=11, tzinfo=timezone.utc),
    dt_to=datetime(year=2024, month=5, day=9, tzinfo=timezone.utc),
    count_candles=585,
    dt_first_candle=datetime(2021, 12, 16, 21, tzinfo=timezone.utc),
    dt_last_candle=datetime(2024, 5, 7, 21, tzinfo=timezone.utc),
    interval=MoexCandleInterval.DAY
)


test_instruments = [SBER, CNTL]
dataset_candles = [
    (SBER, CASE_SBER_FULL_RANGE_EXISTS),
    (CNTL, CASE_CNTL_FULL_RANGE_EXISTS),
    (CNTL, CASE_CNTL_GAP_IN_THE_BEGINNING),
    (CNTL, CASE_CNTL_GAP_IN_THE_END),
    (POSI, CASE_POSI_GAPS_EVERYWHERE)
]
