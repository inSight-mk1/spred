# coding=utf-8
from __future__ import print_function, absolute_import
from gm.api import *
import numpy as np
import pandas as pd
import datetime
import pickle
from tqdm import tqdm

from select_zulu import get_relative_strength


# 可以直接提取数据，掘金终端需要打开，接口取数是通过网络请求的方式，效率一般，行情数据可通过subscribe订阅方式
# 设置token， 查看已有token ID,在用户-秘钥管理里获取
set_token('479feb80f2d2bd55461465e2cfac0be64eba0e98')


def get_normal_stocks(date, new_days=400, skip_suspended=True, skip_st=True):
    """
    获取目标日期date的A股代码（剔除停牌股、ST股、次新股（365天））
    :param date：目标日期
    :param new_days:新股上市天数，默认为365天
    """
    date = pd.Timestamp(date).replace(tzinfo=None)
    # A股，剔除停牌和ST股票
    stocks_info = get_symbols(sec_type1=1010, sec_type2=101001, skip_suspended=skip_suspended, skip_st=skip_st, trade_date=date.strftime('%Y-%m-%d'), df=True)
    stocks_info['listed_date'] = stocks_info['listed_date'].apply(lambda x:x.replace(tzinfo=None))
    stocks_info['delisted_date'] = stocks_info['delisted_date'].apply(lambda x:x.replace(tzinfo=None))
    # 剔除次新股和退市股
    stocks_info = stocks_info[(stocks_info['listed_date']<=date-datetime.timedelta(days=new_days))&(stocks_info['delisted_date']>date)]
    all_stocks = list(stocks_info['symbol'])
    all_stocks_str = ','.join(all_stocks)
    return all_stocks, all_stocks_str


if __name__ == '__main__':
    write_mode = True
    date = '2022-06-06'  # get_normal_stocks函数需要确切的时间，不可为None

    stock_list_filename = date + '_list.pl'
    rs_filename = date + '_rs.pl'

    if write_mode:
        all_stock, all_stock_str = get_normal_stocks(date)

        with open(stock_list_filename, 'wb') as file:
            pickle.dump(all_stock, file)

        # rs选股
        # 先获取基准指数的表现，rs_min选股默认使用1、3、12个月的相对强度
        # 相对强度功能需要
        index_symbol = 'SHSE.000300'
        n_list = [250]
        history_n_count = max(n_list) + 1
        index_history_data = history_n(symbol=index_symbol, frequency='1d', count=history_n_count, end_time=date,
                                       fields='close', adjust=ADJUST_PREV, df=False)
        rs_list = []
        for symbol in tqdm(all_stock):
            rsn = get_relative_strength(symbol, index_history_data, n_list, date)
            rs_list.append(rsn[0])

        with open(rs_filename, 'wb') as file:
            pickle.dump(rs_list, file)

    rs_array = np.array(rs_list)
    max_indices = rs_array.argsort()[::-1]
    max100_indices = max_indices[:100]

    for idx in max100_indices:
        print(all_stock[idx], rs_array[idx])
