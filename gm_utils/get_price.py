# coding=utf-8
from __future__ import print_function, absolute_import
from gm.api import *


# 可以直接提取数据，掘金终端需要打开，接口取数是通过网络请求的方式，效率一般，行情数据可通过subscribe订阅方式
# 设置token， 查看已有token ID,在用户-秘钥管理里获取
set_token('479feb80f2d2bd55461465e2cfac0be64eba0e98')

date = "2022-11-24"
sym = '300662'

if sym[0] == '6':
    full_sym = 'SHSE.' + sym
else:
    full_sym = 'SZSE.' + sym

history_data = history(symbol=full_sym, frequency='1d', start_time=date, end_time=date,
                       fields='open, close, low, high, eob', adjust=ADJUST_NONE, df=True)

print(history_data)