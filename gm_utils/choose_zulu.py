# coding=utf-8
from __future__ import print_function, absolute_import
from gm.api import *
import numpy as np


# 可以直接提取数据，掘金终端需要打开，接口取数是通过网络请求的方式，效率一般，行情数据可通过subscribe订阅方式
# 设置token， 查看已有token ID,在用户-秘钥管理里获取
set_token('479feb80f2d2bd55461465e2cfac0be64eba0e98')


def get_peg(sym, date):
    if sym[0] == '6':
        full_sym = 'SHSE.' + sym
    else:
        full_sym = 'SZSE.' + sym

    pe = stk_get_daily_valuation(symbol=full_sym, fields='pe_ttm,pe_lyr,pe_mrq',
                                 start_date=date, end_date=date, df=False)
    pe_ttm = pe[0]['pe_ttm']

    profit_yoy = stk_get_finance_deriv(symbol=full_sym, fields='net_prof_pcom_yoy, net_prof_pcom_cut_yoy',
                                       rpt_type=None, data_type=None, start_date=date, end_date=date, df=False)
    net_prof_nocut_yoy = profit_yoy[0]['net_prof_pcom_yoy']

    peg = pe_ttm / net_prof_nocut_yoy

    print('peg =', peg)


def get_relative_strength(symbol, index_history_data, n_list, date):
    if symbol[0] == '6':
        full_sym = 'SHSE.' + symbol
    else:
        full_sym = 'SZSE.' + symbol
    history_n_count = max(n_list) + 1
    stock_history_data = history_n(symbol=full_sym, frequency='1d', count=history_n_count, end_time=date,
                                   fields='close', adjust=ADJUST_PREV, df=False)
    rsn = []
    for n in n_list:
        stock_ratio = stock_history_data[-1]['close'] / stock_history_data[-1-n]['close']
        index_ratio = index_history_data[-1]['close'] / index_history_data[-1-n]['close']
        rs = stock_ratio / index_ratio
        rsn.append(rs)
    return rsn


def get_multi_ma(symbol, date, ma, count):
    if symbol[0] == '6':
        full_sym = 'SHSE.' + symbol
    else:
        full_sym = 'SZSE.' + symbol
    history_n_count = ma + count - 1
    history_data = history_n(symbol=full_sym, frequency='1d', count=history_n_count, end_time=date,
                             fields='close', adjust=ADJUST_PREV, df=False)
    close_prices = []
    for data in history_data:
        close = data['close']
        close_prices.append(close)
    close_prices_array = np.array(close_prices)
    man = []
    # 返回的ma是从最远到最近的，按照使用习惯排序，即man[-1]为最近一天的ma价
    for i in range(count):
        ma_price = np.mean(close_prices_array[i:i+ma])
        man.append(ma_price)

    return man


if __name__ == '__main__':
    date = None
    while True:
        # 相对强度功能需要
        # index_symbol = 'SHSE.000985'
        # n_list = [20, 60, 250]
        # history_n_count = max(n_list) + 1
        # stock_history_data = history_n(symbol=index_symbol, frequency='1d', count=history_n_count, end_time=date,
        #                                fields='close', adjust=ADJUST_PREV, df=False)
        sym = input('symbol: ')
        if len(sym):
            print(get_multi_ma(sym, date, ma=5, count=3))
            # print(get_relative_strength(sym, stock_history_data, n_list, date))  # 获取相对强度
        else:
            break

    print('End')
