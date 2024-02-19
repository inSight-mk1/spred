# coding=utf-8
from __future__ import print_function, absolute_import
from gm.api import *


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


date = None
while True:
    sym = input('symbol: ')
    if len(sym):
        get_peg(sym, date)
    else:
        break

print('End')
