# coding=utf-8
from __future__ import print_function, absolute_import
from gm.api import *
import numpy as np

from select_zulu import get_relative_strength


# 可以直接提取数据，掘金终端需要打开，接口取数是通过网络请求的方式，效率一般，行情数据可通过subscribe订阅方式
# 设置token， 查看已有token ID,在用户-秘钥管理里获取
set_token('479feb80f2d2bd55461465e2cfac0be64eba0e98')



if __name__ == '__main__':
    # date = '2019-02-11'
    date = None  # 默认today
    num = 5
    securities_ind = 'SZSE.399975'

    cons = stk_get_index_constituents(securities_ind, trade_date=date)
    additional_symbols = ['SZSE.300033', 'SHSE.601519', 'SHSE.601059', 'SHSE.688318']  # 同花顺、大智慧、信达证券、财富趋势
    symbols = cons['symbol'].to_list()
    for sym in additional_symbols:
        if sym not in symbols:
            symbols.append(sym)

    # rs选股
    # 先获取基准指数的表现，rs_min选股默认使用1、3、12个月的相对强度
    # 相对强度功能需要
    index_symbol = 'SHSE.000300'
    n_list = [5]
    history_n_count = max(n_list) + 1
    index_history_data = history_n(symbol=index_symbol, frequency='1d', count=history_n_count, end_time=date,
                                   fields='close', adjust=ADJUST_PREV, df=False)

    rs_list = []
    for symbol in symbols:
        rsn = get_relative_strength(symbol, index_history_data, n_list, date)
        rs_list.append(rsn[0])
    rs_array = np.array(rs_list)
    max_indices = rs_array.argsort()[::-1]
    top_n_indices = max_indices[:num]
    to_buy = []
    for idx in top_n_indices:
        if rs_array[idx] > 0:
            to_buy.append(symbols[idx])
    print(rs_array[top_n_indices])
    print(to_buy)
