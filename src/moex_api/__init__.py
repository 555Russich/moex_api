import asyncio

from aiohttp import ClientSession


DOMAIN = 'https://iss.moex.com/iss'
DATE_FROM = '28.07.23'
MOEX_indexes = {'химии и нефтехимии': 'MOEXCH', 'потребительский': 'MOEXCN',
                'электроэнергетики': 'MOEXEU', 'финансовый': 'MOEXFN', 'информационных технологий': 'MOEXIT',
                'металлов и добычи': 'MOEXMM', 'нефти и газа': 'MOEXOG', 'строительных компаний': 'MOEXRE',
                'телекоммуникаций': 'MOEXTL', 'транспорта': 'MOEXTN'}


class MOEX:
    _session: ClientSession

    async def get_index_composition(self, index: str) -> list[str]:
        response = await self._get(f'/statistics/engines/stock/markets/index/analytics/{index}',
                                   params={'limit': 100})
        analytics = response['analytics']
        columns = analytics['columns']
        data = analytics['data']
        idx_ticker = columns.index('ticker')
        # print(data)
        return [row[idx_ticker] for row in data]

    async def get_TQBR_tickers(self) -> list[str]:
        response = await self._get(f'/engines/stock/markets/shares/boards/TQBR/securities')
        return [y[0] for y in response['securities']['data']]

    async def _get(self, href: str, params: dict[str, str | int] | None = None):
        async with self._session.get(url=f'{DOMAIN}{href}.json', params=params) as response:
            return await response.json()

    async def __aenter__(self):
        self._session = await ClientSession().__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._session.close()

def get_all_rus_shares():
    try:
        j = flatten(query(f'/engines/stock/markets/shares/boards/TQBR/securities'), 'securities')
    except requests.exceptions.ConnectionError as e:
        print('Repeating request to MOEX API')
        j = flatten(query(f'/engines/stock/markets/shares/boards/TQBR/securities'), 'securities')
    return [row['SECID'] for row in j]


async def main():
    async with MOEX() as moex:
        print(moex._session)
        # imoex = await moex.get_index_composition('IMOEX')
        tickers = await moex.get_rus_shares()
        print(tickers)

if __name__ == '__main__':
    asyncio.run(main())
