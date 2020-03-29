# encoding=utf8

import tushare as ts
import numpy as np
import pandas as pd
import os
import time, datetime
from datetime import datetime as datet

from config import config_private as cfgp

import sys
reload(sys)
sys.setdefaultencoding('utf8')

class Fin_Report_Acquirer(object):
    def __init__(self, ts_code, date):
        self.ts_code = ts_code
        self.date = date
        self.ts_api = None
        self.good_type_str = '预增'

    def init_ts(self):
        my_token = cfgp.my_token
        ts.set_token(my_token)
        self.ts_api = ts.pro_api()

    # Fin_report published on Sat actually influences stock prices on Mon
    def adjust_date(self):
        current_time = time.strptime(self.date, "%Y%m%d")
        if current_time.tm_wday == 0:
            current_datetime = datet.strptime(self.date, "%Y%m%d")
            twodays = datetime.timedelta(days=2)
            true_day = current_datetime - twodays
            self.date = true_day.strftime("%Y%m%d")
        return self.date

    # return True if profit raises
    def acquire_fin_report_status(self):
        self.init_ts()
        self.adjust_date()
        df = self.ts_api.forecast(ts_code=self.ts_code, ann_date=self.date)
        if self.good_type_str in df['type']:
            return True
        df = self.ts_api.express(ts_code=self.ts_code, ann_date=self.date)
        if not df.empty:
            if df['yoy_eps'][0] > 0.0:   # 同比eps增长率
                return True
        df = self.ts_api.fina_indicator(ts_code=self.ts_code, ann_date=self.date)
        if not df.empty:
            if df['basic_eps_yoy'][0] > 0.0:
                return True
        return False


if __name__ == '__main__':
    fra = Fin_Report_Acquirer(ts_code='000661.SZ', date='20200327')
    print(fra.adjust_date())
    print(fra.acquire_fin_report_status())
