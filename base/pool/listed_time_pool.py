from base.pool.stock_pool import StockPool


class ListedTimePool(StockPool):
    def __init__(self, data_path, listed_time=0):
        super().__init__(data_path)
        self.listed_time = listed_time
        self.pool = self.generate_pool()

    def generate_pool(self):
        listed_time_pool = []
        for df in self.all_data:
            if len(df) > self.listed_time:
                listed_time_pool.append(df)
        return listed_time_pool


if __name__ == '__main__':
    pool = ListedTimePool(data_path='./data')
    print(pool.pool[-1])
