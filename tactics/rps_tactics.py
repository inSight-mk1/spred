from choices.rps_choices import RPSChoices
from tushare_utils.get_basic_info import BasicInfoAcquirer
from tushare_utils.get_hk_hold import HkHoldAcquirer
from tushare_utils.get_stock_name import StockNameAcquirer
import numpy as np


class RPSTactics(object):
    def __init__(self, rps_n=50, new_high_t=20):
        self.rps_n = rps_n
        self.new_high_t = new_high_t

    def select(self):
        choices = RPSChoices()
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
                    print(ts_code, stock_name, trade_date, choices.selected_rps_list[i])
            except KeyError:
                print('KeyError')
                print(stock)


if __name__ == '__main__':
    tactics = RPSTactics()
    tactics.select()
