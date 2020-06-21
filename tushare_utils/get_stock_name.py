# encoding=utf8

import tushare as ts
import pandas as pd
from config import config_private as cfgp


class StockNameAcquirer(object):
    def __init__(self, ts_code):
        self.ts_code = ts_code
        self.ts_api = None

        # stock name info need to use as below
        self.name = None

    def init_ts(self):
        my_token = cfgp.my_token
        ts.set_token(my_token)
        self.ts_api = ts.pro_api()

    def acquire_stock_name(self):
        self.init_ts()
        # read info to dataframe
        df = self.ts_api.namechange(ts_code=self.ts_code, fields='ts_code,name,start_date,end_date,change_reason')
        # get info we need
        if df.empty:
            self.name = ''
        else:
            self.name = df['name'][0]


if __name__ == '__main__':
    # Test
    sna = StockNameAcquirer(ts_code='300059.SZ')
    sna.acquire_stock_name()
    print(sna.name)
