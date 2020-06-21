# encoding=utf8

import os
import tushare as ts
import pandas as pd
from config import config_private as cfgp


class HkHoldAcquirer(object):
    def __init__(self, ts_code):
        self.ts_code = ts_code
        self.ts_api = None
        self.hk_data_path = os.path.join(cfgp.save_path, 'hk_hold_info.csv')

        # hk_hold info need to use as below
        self.hk_hold_ratio = None

    def init_ts(self):
        my_token = cfgp.my_token
        ts.set_token(my_token)
        self.ts_api = ts.pro_api()

    def acquire_hk_hold(self):
        self.init_ts()
        # read info to dataframe
        df = pd.read_csv(self.hk_data_path)
        df_need = df[df['ts_code'].isin([self.ts_code])]
        dict_need = df_need.to_dict(orient='ratio')
        # print(dict_need)
        # get info we need
        if len(dict_need) == 0:
            self.hk_hold_ratio = 0.0
        else:
            self.hk_hold_ratio = dict_need[0]['ratio']

    # Return true if good
    def hk_hold_judge(self, min_thresh=2.97):
        # judge whether a stock is good by market value
        if min_thresh <= self.hk_hold_ratio:
            return True
        else:
            return False


if __name__ == '__main__':
    # Test
    hha = HkHoldAcquirer(ts_code='300767.SZ')
    hha.acquire_hk_hold()
    print(hha.hk_hold_ratio)
    print(hha.hk_hold_judge())
