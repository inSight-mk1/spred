from base.pool.stock_pool import StockPool
import numpy as np
from collections import Counter


class ListedTimePool(StockPool):
    def __init__(self, reused_pool=None, listed_time=250, t=0):
        if reused_pool is None:
            super().__init__()
        else:
            self.all_data = reused_pool.all_data
        self.listed_time = listed_time
        self.t = t
        self.pool = self.generate_pool()

    def generate_pool(self):
        listed_time_pool = []
        dates = []
        for df in self.all_data:
            if len(df) > self.listed_time + self.t:
                df_need = np.array(df['trade_date'])
                trade_date = df_need[self.t]
                dates.append(trade_date)
        most_date = Counter(dates).most_common(1)[0][0]
        for df in self.all_data:
            if len(df) > self.listed_time + self.t:
                df_need = np.array(df['trade_date'])
                trade_date = df_need[self.t]
                if trade_date != most_date:
                    continue
                listed_time_pool.append(df[self.t:])
        print(most_date, len(listed_time_pool))
        return listed_time_pool


if __name__ == '__main__':
    pool = ListedTimePool(t=1)
    print(pool.pool[-1])
