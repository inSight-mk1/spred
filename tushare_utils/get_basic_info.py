# encoding=utf8

import tushare as ts
import numpy as np
import pandas as pd
import os
import time
import datetime
from datetime import datetime as datet

from config import config_private as cfgp


class BasicInfoAcquirer(object):
    def __init__(self, ts_code, date):
        self.ts_code = ts_code
        self.date = date
        self.ts_api = None

        # basic info need to use as below
        self.total_mv = None

    def init_ts(self):
        my_token = cfgp.my_token
        ts.set_token(my_token)
        self.ts_api = ts.pro_api()

    def acquire_basic_info(self):
        self.init_ts()
        # read info to dataframe
        df = self.ts_api.daily_basic(ts_code=self.ts_code, trade_date=self.date,
                                     fields='total_mv')
        # get info we need
        self.total_mv = df['total_mv'][0]

    # Return true if good
    def mv_judge(self, min_thresh=3000000, max_thresh=999999999):
        # judge whether a stock is good by market value
        if min_thresh <= self.total_mv <= max_thresh:
            return True
        else:
            return False


if __name__ == '__main__':
    # Test
    bia = BasicInfoAcquirer(ts_code='300767.SZ', date='20200617')
    bia.acquire_basic_info()
    print(bia.total_mv)
    print(bia.mv_judge())
    pass
