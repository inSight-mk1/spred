from choices.rps_choices import RPSChoices
from tushare_utils.get_basic_info import BasicInfoAcquirer
from tushare_utils.get_hk_hold import HkHoldAcquirer
from tushare_utils.get_stock_name import StockNameAcquirer
from tushare_utils.get_ma import MAAcquirer
import numpy as np


class RPSTactics(object):
    def __init__(self, rps_n=50, new_high_t=20, hold_cnt=8, sold_ma=10):
        self.rps_n = rps_n
        self.new_high_t = new_high_t
        self.hold_cnt = hold_cnt
        self.hold_list = []
        self.sold_ma = sold_ma

    def select(self, select_cnt, current_date):
        choices = RPSChoices()
        selected_list = []
        print(len(choices.selected_pool))
        for i, stock in enumerate(choices.selected_pool):
            try:
                if choices.selected_rps_list[i] < 93:
                    df_need = np.array(stock[['ts_code', 'trade_date']])
                    ts_code = str(df_need[0][0])
                    trade_date = str(df_need[0][1])
                    # hk_hold_date = str(df_need[1][1])
                    bia = BasicInfoAcquirer(ts_code, trade_date)
                    bia.acquire_basic_info()
                    if not bia.mv_judge():
                        continue
                    # hha = HkHoldAcquirer(ts_code, hk_hold_date)
                    # hha.acquire_hk_hold()
                    # if not hha.hk_hold_judge():
                    #     continue
                    sna = StockNameAcquirer(ts_code)
                    sna.acquire_stock_name()
                    stock_name = sna.name
                    if trade_date != current_date:
                        continue
                    print(ts_code, stock_name, trade_date, choices.selected_rps_list[i])
                    selected_list.append(dict(ts_code=ts_code, rps=choices.selected_rps_list[i]), trade_date=trade_date)
            except KeyError:
                print('KeyError')
                print(stock)
        selected_list = sorted(selected_list, key=lambda s: s['rps'])
        return selected_list[:select_cnt]

    def buy(self, stock_list):
        for stock in stock_list:
            self.hold_list.append(stock)

    def sold(self):
        sold_indices = []
        for stock, i in enumerate(self.hold_list):
            ts_code = stock['ts_code']
            stock_maa = MAAcquirer(ts_code=ts_code, ma=20)
            stock_maa.acquire_ma()
            if stock_maa.current_price < stock_maa.price_ma:
                sold_indices.append(i)
        for idx in sold_indices:
            self.hold_list.pop(idx)


if __name__ == '__main__':
    tactics = RPSTactics()
    print(tactics.select(select_cnt=2, current_date='20200624'))
