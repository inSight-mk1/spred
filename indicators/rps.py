import numpy as np


class RPS(object):
    def __init__(self, n, stock_pool):
        self.n = n
        self.stock_pool = stock_pool
        self.rps_array = self.cal_rps()

    def cal_rps(self):
        total_cnt = len(self.stock_pool)
        rps_ratio = 100 / total_cnt
        price_ratio_list = []
        for stock in self.stock_pool:
            df_need = np.array(stock[['close']])
            current_price = df_need[0][0]
            n_price = df_need[self.n][0]
            price_ratio = current_price / n_price
            price_ratio_list.append(price_ratio)
        price_ratio_array = np.array(price_ratio_list)
        sort_result = np.argsort(-price_ratio_array)
        rps = sort_result * rps_ratio
        return rps


if __name__ == '__main__':
    from base.pool.listed_time_pool import ListedTimePool
    pool_obj = ListedTimePool()
    pool = pool_obj.pool
    rps_calculator = RPS(250, pool)
    rps_array = rps_calculator.rps_array
    rps_result_list = []
    for i, stock in enumerate(pool):
        df_need = np.array(stock[['ts_code']])
        ts_code = df_need[0][0]
        rps_result = str(ts_code) + ' ' + str(rps_array[i])
        rps_result_list.append(rps_result)
    rps_result_str = '\n'.join(rps_result_list)
    rps_result_file = 'rps.txt'
    with open(rps_result_file, 'w') as f:
        f.write(rps_result_str)
