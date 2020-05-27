from indicators.rps import RPS
from base.pool.listed_time_pool import ListedTimePool


class RPSChoices(object):
    def __init__(self, rps_n=50, thresh=87.0, new_high_t=20):
        # 1. get stock pool
        self.stock_pool = ListedTimePool().pool

        # 2. define indicators
        self.indicators = RPS(n=rps_n, cal_period=new_high_t, stock_pool=self.stock_pool)

        # 3. stock select
        self.selected_pool = self.select()

    def select(self):
        self.indicators.rps_array

