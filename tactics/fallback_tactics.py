from tools.read_forks_pool import read_forks_pool
from base.pool.listed_time_pool import ListedTimePool
from tushare_utils.get_trade_days import get_trade_days


class FallbackTactics(object):
    def __init__(self):
        self.pool = ListedTimePool(data_path='./data')

    def playback(self, start_date, end_date):
        trade_days = get_trade_days(start_date, end_date)



if __name__ == '__main__':
    fbt = FallbackTactics()
    print(fbt.pool.pool[-1])
