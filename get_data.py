import tushare as ts
import numpy as np
import pandas as pd
import os
import time

from config import config_private as cfgp

import sys
reload(sys)
sys.setdefaultencoding('utf8')

my_token = cfgp.my_token
ts.set_token(my_token)

save_path = cfgp.save_path

start_date = '20100101'
end_date = '20200327'
min_len = 850

max_every_min = 200.0
each_query_time = 60.0 / max_every_min

pro = ts.pro_api()

# No qfq
# df = pro.daily(ts_code='600116.SH',
#                start_date='20160701',
#                end_date='20190614')
all_stock = pro.stock_basic(exchange='',
                            list_status='L',
                            fields='ts_code')

all_array = all_stock['ts_code']

print(all_array)

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
        print("Num: %d, time: %.3f, sleep_cnt: %d") % (i, total_time, sleep_cnt)
        total_time = 0.0
        sleep_cnt = 0
