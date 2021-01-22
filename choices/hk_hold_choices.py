import numpy as np
import tushare as ts
import pandas as pd
import os
import time

from config import config_private as cfgp


class HkHoldChoices(object):
    def __init__(self, start_end_date, t_window=20, buy_t_thres=14):
        self.start_end_date = start_end_date
        self.my_token = cfgp.my_token
        ts.set_token(self.my_token)
        self.pro = ts.pro_api()

        self.t_window = t_window
        self.buy_t_thres = buy_t_thres

    def select(self):
        # 1. Get trade hold, select t_window trade days
        df = self.pro.trade_cal(exchange='', start_date=self.start_end_date[0], end_date=self.start_end_date[1])
        date_cnt = len(df)
        trade_date_cnt = 0
        start_date = ''
        dates = []
        for i in range(1, date_cnt + 1):
            if df['is_open'][date_cnt - i] == 1:
                trade_date_cnt += 1
                date = df['cal_date'][date_cnt - i]
                dates.append(date)
                if trade_date_cnt == self.t_window:
                    start_date = df['cal_date'][date_cnt - i]
                    break
        # df_need = df[df['cal_date'].isin(['20201203'])]
        # print(np.array(df_need)[0][-1])
        dates.reverse()

        # 2. Get T-n hk hold list
        max_every_min = 2
        each_query_time = 60.0 / max_every_min
        hk_hold_arrays = []
        for date in dates:
            start = time.time()
            df = self.pro.hk_hold(trade_date=date)
            df_need = np.array(df[['ts_code', 'ratio']])
            hk_hold_arrays.append(df_need)
            end = time.time()
            quert_t = end - start
            if quert_t < each_query_time:
                print('Sleep ', each_query_time, 's')
                time.sleep(each_query_time)
        candidates = []
        buy_t_cnts = []
        for i in range(len(hk_hold_arrays) - 1):
            t0 = hk_hold_arrays[i]
            t1 = hk_hold_arrays[i + 1]
            t0_length = len(t0)
            for j in range(t0_length):
                ts_code = t0[j][0]
                if 'HK' in ts_code:
                    continue
                t0_hold_ratio = t0[j][1]
                idx_array = np.where(t1 == ts_code)[0]
                if len(idx_array) > 0:
                    t1_idx = idx_array[0]
                else:
                    continue
                # print(ts_code, t1_idx)
                t1_hold_ratio = t1[t1_idx][1]
                if t1_hold_ratio >= t0_hold_ratio and t1_hold_ratio >= 3.0:
                    if ts_code in candidates:
                        cidx = candidates.index(ts_code)
                        buy_t_cnts[cidx] += 1
                    else:
                        candidates.append(ts_code)
                        buy_t_cnts.append(1)
        selected_stock = []
        # print(candidates)
        # print(buy_t_cnts)
        c_cnt = len(candidates)
        for i in range(c_cnt):
            if buy_t_cnts[i] >= self.buy_t_thres:
                selected_stock.append(candidates[i])

        return selected_stock


if __name__ == '__main__':
    start_end_date = ['20201201', '20210121']
    hkc = HkHoldChoices(start_end_date)
    ss = hkc.select()
    print(ss)
