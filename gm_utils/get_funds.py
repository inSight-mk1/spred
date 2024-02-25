# coding=utf-8
from __future__ import print_function, absolute_import
from gm.api import *


# 可以直接提取数据，掘金终端需要打开，接口取数是通过网络请求的方式，效率一般，行情数据可通过subscribe订阅方式
# 设置token， 查看已有token ID,在用户-秘钥管理里获取
set_token('479feb80f2d2bd55461465e2cfac0be64eba0e98')

def get_open_ratio(symbol, current_date):
    # 查询当天开盘高开幅度
    # 先获取研报日期下一个交易日
    next_date = get_next_n_trading_dates(exchange='SHSE', date=current_date, n=1)[0]

    # 查询两日数据
    history_data = history_n(symbol=symbol, frequency='1d', count=2, end_time=next_date,
                             fields='open, close, low, high, eob', adjust=ADJUST_NONE, df=False)
    ratio_str = ''
    if len(history_data):
        last_d_ratio = (history_data[1]['open'] / history_data[0]['close'] - 1) * 100
        ratio_str = '%.1f%%' % last_d_ratio
    return ratio_str


# funds data transfer limit: 300/5min
def get_ratios(sym, date):
    history_data = history_n(symbol=sym, frequency='1d', count=2, end_time=date,
                             fields='open, close, low, high, eob', adjust=ADJUST_NONE, df=False)
    ratio_str = ''
    if len(history_data):
        last_d_ratio = (history_data[1]['close'] / history_data[0]['close'] - 1) * 100
        ratio_str = '%.1f%%' % last_d_ratio

    return ratio_str


def get_multi_funds(syms, date):
    # Some symbols are empty or null
    filtered_symbols = []
    valid_indices = []
    for i, sym in enumerate(syms):
        if len(sym) and sym[0] == 'S':
            filtered_symbols.append(sym)
            valid_indices.append(i)
    funds_dict = stk_get_daily_mktvalue_pt(syms, 'tot_mv', trade_date=date, df=False)


def get_funds(sym, date):
    fundamental = stk_get_daily_mktvalue(sym, fields='tot_mv', start_date=date, end_date=date, df=False)
    history_data = history_n(symbol=sym, frequency='1d', count=2, end_time=date,
                             fields='open, close, low, high, eob', adjust=ADJUST_NONE, df=False)

    fund_str = ''
    if len(fundamental):
        yiyuan = fundamental[0]['tot_mv'] / 100000000
        fund_str = "%.0f" % yiyuan

    ratio_str = ''
    if len(history_data):
        last_d_ratio = (history_data[1]['close'] / history_data[0]['close'] - 1) * 100
        ratio_str = '%.1f%%' % last_d_ratio

    return fund_str, ratio_str


def get_funds_prt(sym, date):
    if sym[0] == '6':
        full_sym = 'SHSE.' + sym
    else:
        full_sym = 'SZSE.' + sym

    fundamental = stk_get_daily_mktvalue(full_sym, fields='tot_mv', start_date=date, end_date=date, df=False)
    history_data = history_n(symbol=full_sym, frequency='1d', count=2, end_time=date,
                             fields='open, close, low, high, eob', adjust=ADJUST_NONE, df=False)

    if len(fundamental):
        print(fundamental[0]['trade_date'])
        yiyuan = fundamental[0]['tot_mv'] / 100000000
        fund_str = "fund = %.0f" % yiyuan
        print(fund_str)
    else:
        print('Funds data not found!')

    if len(history_data):
        print(history_data)
        print(history_data[1]['eob'])
        last_d_ratio = (history_data[1]['close'] / history_data[0]['close'] - 1) * 100
        ratio_str = 'last_d_ratio = %.1f%%' % last_d_ratio
        print(ratio_str)
    else:
        print('Prices data not found!')

    print('')


if __name__ == '__main__':
    date = "2024-02-19"
    # date = None

    while True:
        sym = input('symbol: ')
        if len(sym):
            get_funds_prt(sym, date)
        else:
            break

    print('End')

