from indicators.rps import RPS
from base.pool.listed_time_pool import ListedTimePool
import numpy as np


class RPSChoices(object):
    def __init__(self, reused_pool=None, rps_n=50, thresh_min=87.0, thresh_max=92.0, new_high_t=20, t=0):
        self.reused_pool = reused_pool

        self.thresh_min = thresh_min
        self.thresh_max = thresh_max

        # 1. get stock pool
        print('Loading pool')
        self.stock_pool = ListedTimePool(reused_pool=self.reused_pool, t=t).pool

        # 2. define indicators
        print('Calculating rps')
        self.indicators = RPS(n=rps_n, cal_period=new_high_t, stock_pool=self.stock_pool)

        # 3. stock select
        print('Selecting stock')
        self.selected_pool, self.selected_rps_list = self.select()

    def select(self):
        rps_max = np.max(self.indicators.rps_array, axis=1)
        # print(rps_max.shape)
        latest_rps_array = self.indicators.rps_array[:, 0]
        rps_max_choices = rps_max == latest_rps_array
        rps_value_choices = latest_rps_array >= self.thresh_min
        rps_choices = np.logical_and(rps_max_choices, rps_value_choices)

        idx_num = len(self.stock_pool)
        idx_array = np.arange(0, idx_num, 1)
        choices_idx_array = idx_array[rps_choices]
        choices_idx_list = choices_idx_array.tolist()
        selected_pool = []
        selected_rps_list = []
        for idx in choices_idx_list:
            selected_pool.append(self.stock_pool[idx])
            selected_rps_list.append(latest_rps_array[idx])
        return selected_pool, selected_rps_list


if __name__ == '__main__':
    choices = RPSChoices()
    print(len(choices.selected_pool))
    for i, stock in enumerate(choices.selected_pool):
        try:
            if choices.selected_rps_list[i] < 93:
                df_need = np.array(stock[['ts_code']])
                print(df_need[0], choices.selected_rps_list[i])
        except KeyError:
            print(stock)
