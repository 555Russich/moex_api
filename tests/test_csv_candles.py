import aiofiles
import pytest

from aiohttp import ClientSession

from moex_api.csv_candles import CSVCandles
from tests.dataset import dataset_candles


# noinspection PyPropertyAccess
@pytest.mark.parametrize("instrument,case", dataset_candles)
async def test_download_or_read(instrument, case):
    CSVCandles.filepath = case.filepath

    async with aiofiles.open(case.filepath) as f:
        raw_candles = await f.read()

    try:
        async with ClientSession() as session:
            candles = await CSVCandles.download_or_read(session=session, ticker=instrument.ticker, from_=case.dt_from,
                                                        to=case.dt_to, interval=case.interval)
            assert len(candles) == case.count_candles
            assert candles[0].dt == case.dt_first_candle
            assert candles[-1].dt == case.dt_last_candle
    finally:
        async with aiofiles.open(case.filepath, 'w') as f:
            await f.write(raw_candles)
        pass
