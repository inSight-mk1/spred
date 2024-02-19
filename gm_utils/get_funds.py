# coding=utf-8
from __future__ import print_function, absolute_import
from gm.api import *


# 可以直接提取数据，掘金终端需要打开，接口取数是通过网络请求的方式，效率一般，行情数据可通过subscribe订阅方式
# 设置token， 查看已有token ID,在用户-秘钥管理里获取
set_token('479feb80f2d2bd55461465e2cfac0be64eba0e98')

def get_funds(sym):
    if sym[0] == '6':
        full_sym = 'SHSE.' + sym
    else:
        full_sym = 'SZSE.' + sym

    fundamental = stk_get_daily_mktvalue(full_sym, fields='tot_mv', start_date=date, end_date=date, df=False)
    print(fundamental)
    if len(fundamental):
        print(fundamental[0]['tot_mv'] / 100000000)

date = "2022-11-28"
while True:
    sym = input('symbol: ')
    if len(sym):
        get_funds(sym)
    else:
        break

print('End')

