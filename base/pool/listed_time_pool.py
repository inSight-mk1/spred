from base.pool.stock_pool import StockPool


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
        for df in self.all_data:
            if len(df) > self.listed_time + self.t:
                listed_time_pool.append(df[self.t:])
        return listed_time_pool


if __name__ == '__main__':
    pool = ListedTimePool(t=1)
    print(pool.pool[-1])
