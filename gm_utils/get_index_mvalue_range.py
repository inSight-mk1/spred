# coding=utf-8
from __future__ import print_function, absolute_import
from gm.api import *
import pandas as pd
import datetime


# 可以直接提取数据，掘金终端需要打开，接口取数是通过网络请求的方式，效率一般，行情数据可通过subscribe订阅方式
# 设置token， 查看已有token ID,在用户-秘钥管理里获取
set_token('479feb80f2d2bd55461465e2cfac0be64eba0e98')


def get_normal_stocks(date, new_days=365, skip_suspended=True, skip_st=True):
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


date = '2024-02-27'
# 目前有的指数：
# 中证500：301-800
# 中证1000：801-1800
# 国证2000：1001-3000
# 中证2000：1801-3800 （掘金平台暂无）
# 获取指数会获取到688235这种千亿多的，导致最大指数不准，因此直接从全市场拉股票列表进行市值排序
# index_syms = ['SHSE.000905', 'SHSE.000852', 'SZSE.399303']

m_value_rank_ranges = [[301, 800], [801, 1800], [1801, 3800]]

print(date)
# 获取A股代码（剔除停牌股、ST股、次新股（365天））
all_stock, all_stock_str = get_normal_stocks(date)
# 获取所有股票市值,并按降序排序
fundamental = stk_get_daily_mktvalue_pt(symbols=all_stock, fields='tot_mv', trade_date=date,
                                        df=True).sort_values(by='tot_mv', ascending=False)
funds_array = fundamental['tot_mv'].to_numpy()
for rank_range in m_value_rank_ranges:
    max_mv = funds_array[rank_range[0]] / 100000000
    min_mv = funds_array[rank_range[1]] / 100000000
    print(rank_range[0], '-', rank_range[1], ':', min_mv, max_mv)
