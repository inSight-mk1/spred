from indicators.rps import RPS
from base.pool.listed_time_pool import ListedTimePool
import numpy as np


class RPSChoices(object):
    def __init__(self, rps_n=50, thresh=87.0, new_high_t=20):
        self.thresh = thresh
        # 1. get stock pool
        self.stock_pool = ListedTimePool().pool

        # 2. define indicators
        self.indicators = RPS(n=rps_n, cal_period=new_high_t, stock_pool=self.stock_pool)

        # 3. stock select
        self.selected_pool = self.select()

    def select(self):
        rps_array = self.indicators.rps_array
        rps_max = np.max(rps_array, axis=1)
        current_max = (rps_max == rps_array[:, 0])
        rps_good = (rps_max >= self.thresh)
        # print(current_max.shape, rps_good.shape)
        selected_map = np.logical_and(current_max, rps_good)
        # print(selected_map)
        selected_pool = []
        for i, stock in enumerate(self.stock_pool):
            if selected_map[i]:
                selected_pool.append(stock)
                print(stock['ts_code'][0], 'rps', rps_array[i][0])
        return selected_pool


if __name__ == '__main__':
    choices = RPSChoices()
    print(len(choices.selected_pool))
