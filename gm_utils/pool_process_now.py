# coding=utf-8
import pandas as pd
from gm.api import *
from get_funds import get_funds, get_open_ratio
from tqdm import tqdm

# 可以直接提取数据，掘金终端需要打开，接口取数是通过网络请求的方式，效率一般，行情数据可通过subscribe订阅方式
# 设置token， 查看已有token ID,在用户-秘钥管理里获取
set_token('479feb80f2d2bd55461465e2cfac0be64eba0e98')

if __name__ == '__main__':
    pool = pd.read_excel("stock_pool_all.xls", sheet_name="Now", usecols="A:F")
    pool_null = pool.isnull()
    data_len = len(pool['sym_ch'])
    for i in range(1, data_len):
        if pool_null['date'][i]:
            pool.loc[i, 'date'] = pool.loc[i - 1, 'date']
            pool_null['date'][i] = False
        if pool_null['concept'][i]:
            pool.loc[i, 'concept'] = pool.loc[i - 1, 'concept']
            pool_null['concept'][i] = False

    # Get all symbols on the last trade date
    last_trade_day = pool['date'][data_len - 1]
    yr, mon, day = last_trade_day.split('-')[0].split('.')
    mon = mon.zfill(2)  # '3' -> '03'
    day = day.zfill(2)  # '3' -> '03'
    last_trade_day = '20%s-%s-%s' % (yr, mon, day)
    print(last_trade_day)
    all_symbols = get_symbols(sec_type1=1010, sec_type2=101001, exchanges=['SHSE', 'SZSE'],
                              symbols=None, skip_suspended=False, skip_st=False,
                              trade_date=last_trade_day, df=True)
    # print(all_symbols['sec_name'])

    for i in tqdm(range(0, data_len)):
        sym_ch = pool['sym_ch'][i]
        if not pool_null['sym_ch'][i] and pool_null['symbol'][i]:  # 中文标的名称存在，但不存在标的代码，才需要查询信息
            res = all_symbols[all_symbols['sec_name'].str.contains(sym_ch)]['symbol'].to_string()
            symbol = res.split(' ')[-1]
            if len(res) > 1:
                pool.loc[i, 'symbol'] = symbol
                current_date = pool['date'][i]
                yr, mon, day = current_date.split('-')[0].split('.')
                mon = mon.zfill(2)  # '3' -> '03'
                day = day.zfill(2)  # '3' -> '03'
                current_date = '20%s-%s-%s' % (yr, mon, day)
                fund, ratio = get_funds(symbol, current_date)
                pool.loc[i, 'm_value'] = fund
                pool.loc[i, 'lastd_ratio'] = ratio
                # pool.loc[i, 'open_ratio'] = get_open_ratio(symbol, current_date)

    # pool.to_csv("stock_pool_23.2_full.csv")
    pool.to_excel("stock_pool_now_full.xls", sheet_name="Sheet1")
