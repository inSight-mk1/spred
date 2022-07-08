import tushare as ts
import numpy as np
import pandas as pd
import os
import time

from config import config_private as cfgp
from tools.read_forks_pool import read_forks_pool


def get_price_data(pro, start_date, end_date, save_path, min_len, each_query_time, stock_list=None):
    # No qfq
    # df = pro.daily(ts_code='600116.SH',
    #                start_date='20160701',
    #                end_date='20190614')
    if stock_list is None:
        all_stock = pro.stock_basic(exchange='',
                                    list_status='L',
                                    fields='ts_code')
        all_array = all_stock['ts_code']
        print(all_array)
    else:
        all_array = []
        for code in stock_list:
            if code[0] == '6':
                all_array.append(code + '.SH')
            else:
                all_array.append(code + '.SZ')

    i = 0

    total_time = 0.0
    sleep_cnt = 0
    for ts_code in all_array:
        i += 1

        start = time.time()
        df = ts.pro_bar(ts_code=ts_code,
                        adj='qfq',
                        start_date=start_date,
                        end_date=end_date)
        end = time.time()
        quert_t = end - start
        total_time += quert_t
        if quert_t < each_query_time:
            time.sleep(each_query_time - quert_t)
            sleep_cnt += 1

        fn = ts_code + '.csv'
        fp = os.path.join(save_path, fn)
        if df is not None:
            nd = np.array(df)
            if len(nd) >= min_len:
                df.to_csv(fp, sep=',', header=True, index=True)
        else:
            print("Get dataframe ERROR at " + str(i))
            continue

        if i % 10 == 0:
            print("Num: %d, time: %.3f, sleep_cnt: %d" % (i, total_time, sleep_cnt))
            total_time = 0.0
            sleep_cnt = 0


def get_hk_hold_data(pro, hk_data_date):
    df = pro.hk_hold(trade_date=hk_data_date)
    fn = 'hk_hold_info.csv'
    fp = os.path.join(save_path, fn)
    df.to_csv(fp, sep=',', header=True, index=True)


if __name__ == '__main__':
    my_token = cfgp.my_token
    ts.set_token(my_token)

    save_path = cfgp.save_path

    xlsx_path = './forks_0526.xlsx'
    stock_list = read_forks_pool(xlsx_path)

    start_date = '20220401'
    end_date = '20220624'
    hk_data_date = '20200623'

    min_len = 0

    max_every_min = 500
    each_query_time = 60.0 / max_every_min

    pro = ts.pro_api()

    # get_hk_hold_data(pro, hk_data_date)
    get_price_data(pro, start_date, end_date, save_path, min_len, each_query_time, stock_list)
