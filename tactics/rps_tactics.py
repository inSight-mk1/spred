from choices.rps_choices import RPSChoices
from tushare_utils.get_basic_info import BasicInfoAcquirer
from tushare_utils.get_hk_hold import HkHoldAcquirer
from tushare_utils.get_stock_name import StockNameAcquirer
from tushare_utils.get_ma import MAAcquirer
from base.pool.stock_pool import StockPool
import config.config_thread as config_thread

import numpy as np
import math
from multiprocessing import Pool

# import objgraph


def chunks(arr, m):
    n = int(math.ceil(len(arr) / float(m)))
    return [arr[i:i + n] for i in range(0, len(arr), n)]


def select_part(params):
    selected_pool = params['selected_pool']
    selected_rps_list = params['selected_rps_list']
    selected_list = []
    for i, stock in enumerate(selected_pool):
        try:
            if selected_rps_list[i] < 93:
                df_need = np.array(stock[['ts_code', 'trade_date']])
                ts_code = str(df_need[0][0])
                trade_date = str(df_need[0][1])
                # hk_hold_date = str(df_need[1][1])
                # bia = BasicInfoAcquirer(ts_code, trade_date)
                # bia.acquire_basic_info()
                # if not bia.mv_judge():
                #     continue

                # hha = HkHoldAcquirer(ts_code, hk_hold_date)
                # hha.acquire_hk_hold()
                # if not hha.hk_hold_judge():
                #     continue

                # sna = StockNameAcquirer(ts_code)
                # sna.acquire_stock_name()
                # stock_name = sna.name
                # print(ts_code, stock_name, trade_date, choices.selected_rps_list[i])

                selected_list.append(dict(ts_code=ts_code, rps=selected_rps_list[i], trade_date=trade_date))
        except KeyError:
            print('KeyError')
            print(stock)
    return selected_list


class RPSTactics(object):
    def __init__(self, reused_pool, rps_n=50, thresh_min=87.0, thresh_max=92.0, new_high_t=20, hold_cnt=8, sold_ma=10,
                 t=0, hold_value=1.0):
        self.reused_pool = reused_pool
        self.rps_n = rps_n
        self.thresh_min = thresh_min
        self.thresh_max = thresh_max
        self.new_high_t = new_high_t
        self.hold_cnt = hold_cnt
        self.hold_list = []
        self.sold_ma = sold_ma
        self.t = t
        self.hold_value = hold_value

    def select(self, select_cnt):
        selected_list = []
        if select_cnt == 0:
            return selected_list
        choices = RPSChoices(reused_pool=self.reused_pool, t=self.t, rps_n=self.rps_n,
                             thresh_max=self.thresh_max, thresh_min=self.thresh_min)

        # nthreads = config_thread.rps_sel_nthreads
        # params = []
        # selected_pool_part = chunks(choices.selected_pool, nthreads)
        # selected_rps_list_part = chunks(choices.selected_rps_list, nthreads)
        # nthreads = len(selected_pool_part)
        # print('Actual num of threads', nthreads)
        # for i in range(nthreads):
        #     param_d = dict(selected_pool=selected_pool_part[i],
        #                    selected_rps_list=selected_rps_list_part[i])
        #     params.append(param_d)
        # pool = Pool(nthreads)
        # results = pool.map(select_part, params)
        # for res in results:
        #     selected_list.extend(res)
        # pool.close()

        for i, stock in enumerate(choices.selected_pool):
            try:
                if choices.selected_rps_list[i] < 93:
                    # print(stock)
                    df_need = np.array(stock[['ts_code', 'trade_date', 'close', 'idx', 'time_idx']])
                    ts_code = str(df_need[0][0])
                    trade_date = str(df_need[0][1])
                    selected_price = str(df_need[0][2])
                    stock_idx = df_need[0][3]
                    time_idx = df_need[0][4]
                    # hk_hold_date = str(df_need[1][1])
                    # bia = BasicInfoAcquirer(ts_code, trade_date)
                    # bia.acquire_basic_info()
                    # if not bia.mv_judge():
                    #     continue
                    # hha = HkHoldAcquirer(ts_code, hk_hold_date)
                    # hha.acquire_hk_hold()
                    # if not hha.hk_hold_judge():
                    #     continue
                    # sna = StockNameAcquirer(ts_code)
                    # sna.acquire_stock_name()
                    # stock_name = sna.name
                    # print(ts_code, stock_name, trade_date, choices.selected_rps_list[i])
                    selected_list.append(dict(ts_code=ts_code, rps=choices.selected_rps_list[i], trade_date=trade_date,
                                              selected_price=selected_price, stock_idx=stock_idx, time_idx=time_idx,
                                              hold_value=self.hold_value))
            except KeyError:
                print('KeyError')
                print(stock)
        selected_list = sorted(selected_list, key=lambda s: s['rps'])
        return selected_list[:select_cnt]

    def buy(self, stock_list):
        print('buy: ')
        print(stock_list)
        for stock in stock_list:
            self.hold_list.append(stock)

    def sold(self):
        print('sold: ')
        sold_indices = []
        sold_prices = []
        ratios = []
        for i, stock in enumerate(self.hold_list):
            ts_code = stock['ts_code']
            stock_maa = MAAcquirer(ts_code=ts_code, ma=self.sold_ma, t=self.t)
            stock_maa.acquire_ma()
            # print(ts_code, stock_maa.price_ma)
            if stock_maa.current_price < stock_maa.price_ma:
                sold_indices.append(i)
                sold_prices.append(stock_maa.current_price)
        old_hold_list = self.hold_list
        self.hold_list = []
        sold_list = []
        j = 0
        for i, stock in enumerate(old_hold_list):
            if i not in sold_indices:
                self.hold_list.append(stock)
            else:
                # TODO: Use T+1 open/close price as buy_price
                sold_list.append(old_hold_list[i])
                stock_idx = stock['stock_idx']
                time_idx = stock['time_idx']
                # Get T+1 open/close price
                buy_price = self.reused_pool.get_price(stock_idx, time_idx - 1)
                sold_price = sold_prices[j]
                ratio = (sold_price - buy_price) / buy_price
                ratios.append(ratio)
                print(stock, buy_price, sold_price, ratio)
                j += 1
        print('End of sold')
        return sold_list, ratios

    def update(self):
        self.sold()
        current_hold_cnt = len(self.hold_list)
        target_hold_cnt = self.hold_cnt
        buy_cnt = target_hold_cnt - current_hold_cnt
        selected_list = self.select(select_cnt=buy_cnt)
        self.buy(selected_list)
        return self.hold_list


if __name__ == '__main__':
    reused_pool = StockPool()
    playback_t = 60
    hold_list = []
    for t in range(playback_t, -1, -1):
        print(t)
        tactics = RPSTactics(reused_pool=reused_pool, t=t, sold_ma=20)
        tactics.hold_list = hold_list
        hold_list = tactics.update()
        # objgraph.show_growth()
