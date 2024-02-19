# coding=utf-8
from __future__ import print_function, absolute_import
from gm.api import *


# 可以直接提取数据，掘金终端需要打开，接口取数是通过网络请求的方式，效率一般，行情数据可通过subscribe订阅方式
# 设置token， 查看已有token ID,在用户-秘钥管理里获取
set_token('479feb80f2d2bd55461465e2cfac0be64eba0e98')

def get_funds(sym, date):
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

date = "2024-02-19"
# date = None

while True:
    sym = input('symbol: ')
    if len(sym):
        get_funds(sym, date)
    else:
        break

print('End')

