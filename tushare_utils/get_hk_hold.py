# encoding=utf8

import tushare as ts
import pandas as pd
from config import config_private as cfgp


class HkHoldAcquirer(object):
    def __init__(self, ts_code, date):
        self.ts_code = ts_code
        self.date = date
        self.ts_api = None

        # hk_hold info need to use as below
        self.hk_hold_ratio = None

    def init_ts(self):
        my_token = cfgp.my_token
        ts.set_token(my_token)
        self.ts_api = ts.pro_api()

    def acquire_hk_hold(self):
        self.init_ts()
        # read info to dataframe
        df = self.ts_api.hk_hold(ts_code=self.ts_code, trade_date=self.date)
        # get info we need
        if df.empty:
            self.hk_hold_ratio = 0.0
        else:
            self.hk_hold_ratio = df['ratio'][0]

    # Return true if good
    def hk_hold_judge(self, min_thresh=2.97):
        # judge whether a stock is good by market value
        if min_thresh <= self.hk_hold_ratio:
            return True
        else:
            return False


if __name__ == '__main__':
    # Test
    hha = HkHoldAcquirer(ts_code='300059.SZ', date='20200617')
    hha.acquire_hk_hold()
    print(hha.hk_hold_ratio)
    print(hha.hk_hold_judge())
