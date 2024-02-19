# coding=utf-8
from __future__ import print_function, absolute_import
from gm.api import *


# 可以直接提取数据，掘金终端需要打开，接口取数是通过网络请求的方式，效率一般，行情数据可通过subscribe订阅方式
# 设置token， 查看已有token ID,在用户-秘钥管理里获取
set_token('479feb80f2d2bd55461465e2cfac0be64eba0e98')


def get_openhigh(sym):
    if sym[0] == '6':
        full_sym = 'SHSE.' + sym
    else:
        full_sym = 'SZSE.' + sym

    history_data = history_n(symbol=full_sym, frequency='1d', count=2, end_time=date,
                             fields='open, close, low, high, eob', adjust=ADJUST_NONE, df=False)
    print(history_data)
    if len(history_data):
        openhigh = (history_data[1]['open'] / history_data[0]['close'] - 1) * 100
        print(openhigh)

date = "2022-11-07"
while True:
    sym = input('symbol: ')
    if len(sym):
        get_openhigh(sym)
    else:
        break

print('End')
