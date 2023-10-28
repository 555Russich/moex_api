import asyncio
from datetime import datetime, timedelta
from urllib import parse
import math

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
        print(response)
        analytics = response['analytics']
        columns = analytics['columns']
        data = analytics['data']
        idx_ticker = columns.index('ticker')
        # print(data)
        return [row[idx_ticker] for row in data]

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


def get_index_composition(index: str):
    return pd.DataFrame(
        flatten(query(f'/statistics/engines/stock/markets/index/analytics/{index}.json?limit=100'), 'analytics'))[
        'ticker']


def query(method: str, **kwargs):
    try:
        url = f'https://iss.moex.com/iss{method}.json'
        if kwargs:
            url += "?" + parse.urlencode(kwargs)

        r = requests.get(url, timeout=10)
        r.encoding = 'utf-8'
        j = r.json()
        return j

    except Exception as e:
        raise e


def flatten(j: dict, blockname: str):
    """
    Собираю двумерный массив (словарь)
    :param j:
    :param blockname:
    :return:
    """
    return [{k: r[i] for i, k in enumerate(j[blockname]['columns'])} for r in j[blockname]['data']]


def format_date_list(tradedates: list):
    return [(datetime.strptime(date, '%Y-%m-%d')).strftime('%d.%m.%y') for date in tradedates]


def change_axis_range(l: list, max_len: int):
    l = list(l)
    n = 1
    while len(l) / n > max_len:
        n += 1
    x = [l[i] for i in range(0, len(l), n)]
    if l[-1] != x[-1]: x.append(l[-1])
    return x


async def main():
    async with MOEX() as moex:
        print(moex._session)
        imoex = await moex.get_index_composition('IMOEX')
        print(imoex)
        print(len(imoex))


if __name__ == '__main__':
    asyncio.run(main())
