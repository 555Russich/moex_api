import asyncio

from aiohttp import ClientSession


DOMAIN = 'https://iss.moex.com/iss/'
DATE_FROM = '28.07.23'
MOEX_indexes = {'химии и нефтехимии': 'MOEXCH', 'потребительский': 'MOEXCN',
                'электроэнергетики': 'MOEXEU', 'финансовый': 'MOEXFN', 'информационных технологий': 'MOEXIT',
                'металлов и добычи': 'MOEXMM', 'нефти и газа': 'MOEXOG', 'строительных компаний': 'MOEXRE',
                'телекоммуникаций': 'MOEXTL', 'транспорта': 'MOEXTN'}


class MOEX:
    _session: ClientSession

    async def get_index_composition(self, index: str) -> list[str]:
        response = await self._get(f'statistics/engines/stock/markets/index/analytics/{index}',
                                   params={'limit': 100})
        analytics = response['analytics']
        columns = analytics['columns']
        data = analytics['data']
        idx_ticker = columns.index('ticker')
        # print(data)
        return [row[idx_ticker] for row in data]

    async def get_TQBR_tickers(self) -> list[str]:
        response = await self._get(f'engines/stock/markets/shares/boards/TQBR/securities')
        return [y[0] for y in response['securities']['data']]

    async def get_engines(self) -> ...:
        r = await self._get('engines')
        # columns =

    async def get_markets(self, engine: str) -> None:
        r = await self._get(f'engines/{engine}/markets')
        print(r)

    async def get_candles_default_board(self,  engine: str, market: str, security: str):
        params = {'interval': 1}
        r = await self._get(f'engines/{engine}/markets/{market}/securities/{security}/candles', params=params)
        print(r)

    async def _get(self, href: str, params: dict[str, str | int] | None = None) -> dict:
        async with self._session.get(url=f'{DOMAIN}{href}.json', params=params) as response:
            return await response.json()

    async def __aenter__(self):
        self._session = await ClientSession().__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._session.close()


async def main():
    async with MOEX() as moex:
        print(moex._session)
        # imoex = await moex.get_index_composition('IMOEX')
        # r = await moex.get_engines()
        # r = await moex.get_markets('stock')
        r = await moex.get_candles_default_board(engine='stock', market='shares', security='SBER')
        print(r)

if __name__ == '__main__':
    asyncio.run(main())
