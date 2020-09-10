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
    def __init__(self, reused_pool=None, rps_n=50, new_high_t=20, hold_cnt=8, sold_ma=10, t=0):
        self.reused_pool = reused_pool
        self.rps_n = rps_n
        self.new_high_t = new_high_t
        self.hold_cnt = hold_cnt
        self.hold_list = []
        self.sold_ma = sold_ma
        self.t = t

    def select(self, select_cnt):
        choices = RPSChoices(reused_pool=reused_pool, t=self.t)
        selected_list = []

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
                    selected_list.append(dict(ts_code=ts_code, rps=choices.selected_rps_list[i], trade_date=trade_date))
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
        for i, stock in enumerate(self.hold_list):
            ts_code = stock['ts_code']
            stock_maa = MAAcquirer(ts_code=ts_code, ma=self.sold_ma, t=self.t)
            stock_maa.acquire_ma()
            # print(ts_code, stock_maa.price_ma)
            if stock_maa.current_price < stock_maa.price_ma:
                sold_indices.append(i)
        old_hold_list = self.hold_list
        self.hold_list = []
        for i, stock in enumerate(old_hold_list):
            if i not in sold_indices:
                self.hold_list.append(stock)
            else:
                print(stock)
        print('End of sold')

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
        tactics = RPSTactics(reused_pool=reused_pool, t=t)
        tactics.hold_list = hold_list
        hold_list = tactics.update()
        # objgraph.show_growth()
