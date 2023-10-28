from datetime import datetime, timedelta

import plotly.graph_objs
import requests
from urllib import parse
import math

from matplotlib import pyplot as plt
import dash
import plotly.express as px

import pandas as pd
pd.set_option('display.max_columns', 30)
# pd.set_option('display.max_rows', 300)

MOEX_indexes = {'химии и нефтехимии': 'MOEXCH', 'потребительский': 'MOEXCN',
                'электроэнергетики': 'MOEXEU', 'финансовый': 'MOEXFN', 'информационных технологий': 'MOEXIT',
                'металлов и добычи': 'MOEXMM', 'нефти и газа': 'MOEXOG', 'строительных компаний': 'MOEXRE',
                'телекоммуникаций': 'MOEXTL', 'транспорта': 'MOEXTN'}
DATE_FROM = '28.07.23'


class MOEX:
    @classmethod
    async def get_index_composition(cls, index: str) -> list[str]:


def run():
    # plotly_all_sectors_indexes(MOEX_indexes)
    plot_all_sector_indexes(MOEX_indexes)
    # plot_shares_in_index('MOEXEU')


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


def plot_shares_in_index(index: str):
    shares_tickers = get_index_composition(index)

    n_axis = math.ceil(len(shares_tickers) / 10)
    n_graphics_on_one_axis = math.ceil(len(shares_tickers) / n_axis)

    all_df = {}
    n = 0
    for ticker in shares_tickers:
        all_df[ticker] = one_ticker_df(ticker, ticker_type='share')
        n += 1
        print(f'{n}/{len(shares_tickers)} tickers histories got')

    df_index = one_ticker_df(index, ticker_type='index')

    n_graphics_plotes = 0
    if n_axis < 3:
        fig = plt.figure(n_axis)
        n_subplot_x = 1
        n_subplot_y = 1
        for i in range(n_axis):
            ax = fig.add_subplot(n_axis, n_subplot_x, n_subplot_y)
            ax.plot(df_index['DATES'], df_index['PERCENTAGE'], label=index, color='black', linestyle='--')

            for ticker in shares_tickers[n_graphics_plotes:n_graphics_on_one_axis + n_graphics_plotes]:
                x = change_axis_range(all_df[ticker]['DATES'], 21)
                ax.plot(all_df[ticker]['DATES'], all_df[ticker]['PERCENTAGE'], label=ticker)
                ax.set_xticks(x)
            n_graphics_plotes += n_graphics_on_one_axis
            if i % 2:
                n_subplot_x += 1
            else:
                n_subplot_y += 1
            ax.grid(True)
            ax.legend(fontsize=8)
        plt.show()
    else:
        for i in range(n_axis):
            plt.figure()
            plt.plot(df_index['DATES'], df_index['PERCENTAGE'], label=index, color='black', linestyle='--')
            for ticker in shares_tickers[n_graphics_plotes:n_graphics_on_one_axis + n_graphics_plotes]:
                x = change_axis_range(all_df[ticker]['DATES'], 21)
                plt.plot(all_df[ticker]['DATES'], all_df[ticker]['PERCENTAGE'], label=ticker)
                plt.xticks(x)
                plt.grid()
                plt.legend(fontsize=8)
            n_graphics_plotes += n_graphics_on_one_axis
        plt.show()


def plot_all_sector_indexes(names_and_sectors: dict):
    all_df = {}
    n = 0
    for index in names_and_sectors.values():
        all_df[index] = one_ticker_df(index, ticker_type='index')
        n += 1
        print(f'{n}/{len(names_and_sectors)} indices history got')

    df = one_ticker_df('IMOEX', ticker_type='index')
    plt.plot(df['DATES'], df['PERCENTAGE'], label='IMOEX', color='black', linestyle='--')

    for name, index in names_and_sectors.items():
        x = change_axis_range(all_df[index]['DATES'], 21)
        plt.plot(all_df[index]['DATES'], all_df[index]['PERCENTAGE'], label=name)
        plt.xticks(x)

    plt.grid()
    plt.legend(fontsize=8)
    plt.show()


def plotly_all_sectors_indexes(names_and_sectors: dict):
    main_index = 'IMOEX'

    all_df = {}
    n = 0
    for index in names_and_sectors.values():
        all_df[index] = one_ticker_df(index, ticker_type='index')
        n += 1
        print(f'{n}/{len(names_and_sectors)} indices history got')

    fig = plotly.graph_objs.Figure()

    df = one_ticker_df(main_index, ticker_type='index')
    fig.add_scatter(x=df['DATES'],
                    y=df['PERCENTAGE'],
                    name=main_index,
                    line={'color': 'black', 'dash': 'dash'})

    for name, index in names_and_sectors.items():
        fig.add_scatter(x=all_df[index]['DATES'],
                        y=all_df[index]['PERCENTAGE'],
                        name=name)

    fig.update_layout(title={'text': f'График отраслевых индексов Московской биржи'},
                      xaxis={'tickvals': change_axis_range(df['DATES'], 30)})

    config = {'scrollZoom': True,
              'toImageButtonOptions': {
                   'format': 'jpeg',  # one of png, svg, jpeg, webp
                   'filename': f'{main_index}_sectors_{df["DATES"].iloc[-1]}',
                   'height': 1080,
                   'width': 1920,
                   'scale': 1},  # Multiply title/legend/axis/canvas sizes by this factor
              'modeBarButtonsToAdd': ['drawline',
                                      'drawopenpath',
                                       # 'drawclosedpath',
                                       # 'drawcircle',
                                       'drawrect',
                                       'eraseshape']
              }

    fig.show(config=config)


def one_ticker_df(ticker: str, date_from=DATE_FROM, date_till=datetime.now(), ticker_type='index'):

    date_from_ = (date_till - timedelta(days=30)).strftime('%Y-%m-%d')
    date_from = datetime.strptime(date_from, '%d.%m.%y').strftime('%Y-%m-%d')
    date_till = date_till.strftime('%Y-%m-%d')

    if ticker_type == 'index':
        method = f'/history/engines/stock/markets/index/securities/{ticker}.json?from={date_from_}&till={date_till}'
    elif ticker_type == 'share':
        method = f'/history/engines/stock/markets/shares/boards/TQBR/securities/{ticker}.json?from={date_from_}&till={date_till}'
    j = query(method)
    last_date = pd.DataFrame(flatten(j, 'history'))['TRADEDATE'].iloc[-1]

    df_list = []
    while date_from < date_till:
        if ticker_type == 'index':
            method = f'/history/engines/stock/markets/index/securities/{ticker}.json?from={date_from}&till={date_till}'
        elif ticker_type == 'share':
            method = f'/history/engines/stock/markets/shares/boards/TQBR/securities/{ticker}.json?from={date_from}&till={date_till}'
        j = query(method)
        df = pd.DataFrame(flatten(j, 'history'))

        if df_list: df = df.drop(index=0)

        if last_date == df['TRADEDATE'].iloc[-1]:
            date_from = date_till
        else:
            date_from = df['TRADEDATE'].iloc[-1]

        df_list.append(df)

    df = pd.concat(df_list, ignore_index=True)
    df['DATES'] = format_date_list(df['TRADEDATE'])
    df['PERCENTAGE'] = [(x / df['CLOSE'][0]) * 100 - 100 for x in df['CLOSE']]
    return df


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


def main():
    run()


if __name__ == '__main__':
    main()
