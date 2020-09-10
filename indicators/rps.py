import numpy as np
import math
from multiprocessing import Pool

import config.config_thread as config_thread


def chunks(arr, m):
    n = int(math.ceil(len(arr) / float(m)))
    return [arr[i:i + n] for i in range(0, len(arr), n)]


def cal_rps_part(params):
    cal_period = params['cal_period']
    stock_pool = params['stock_pool']
    n = params['n']
    rps_ratio = params['rps_ratio']
    rps_period = []
    for i in cal_period:
        price_ratio_list = []
        for stock in stock_pool:
            # print(i)
            try:
                df_need = np.array(stock[['close']])
            except KeyError:
                print(i, stock)
            current_price = df_need[i][0]
            n_price = df_need[n][0]
            price_ratio = current_price / n_price
            price_ratio_list.append(price_ratio)
        price_ratio_array = np.array(price_ratio_list)
        order = np.argsort(price_ratio_array)
        ranks = np.argsort(order)
        rps = ranks * rps_ratio
        rps_list = rps.tolist()
        rps_period.append(rps_list)
    return rps_period


class RPS(object):
    def __init__(self, n, cal_period, stock_pool: list):
        self.n = n
        self.cal_period = cal_period
        self.stock_pool = stock_pool
        self.rps_array = self.cal_rps()

    def cal_rps(self):
        total_cnt = len(self.stock_pool)
        rps_ratio = 100 / total_cnt
        rps_period = []
        nthreads = config_thread.rps_cal_nthreads
        params = []
        parts_cal_period = chunks(range(self.cal_period), nthreads)
        nthreads = len(parts_cal_period)
        print('Actual num of threads', nthreads)
        for i in range(nthreads):
            param_d = dict(cal_period=parts_cal_period[i],
                           stock_pool=self.stock_pool,
                           rps_ratio=rps_ratio,
                           n=self.n)
            params.append(param_d)
        pool = Pool(nthreads)
        results = pool.map(cal_rps_part, params)
        for res in results:
            rps_period.extend(res)
        pool.close()
        # for i in range(self.cal_period):
        #     # print('last one', self.stock_pool[-1])
        #     price_ratio_list = []
        #     for stock in self.stock_pool:
        #         # print(i)
        #         try:
        #             df_need = np.array(stock[['close']])
        #         except KeyError:
        #             print(i, stock)
        #         current_price = df_need[i][0]
        #         n_price = df_need[self.n][0]
        #         price_ratio = current_price / n_price
        #         price_ratio_list.append(price_ratio)
        #     price_ratio_array = np.array(price_ratio_list)
        #     order = np.argsort(price_ratio_array)
        #     ranks = np.argsort(order)
        #     rps = ranks * rps_ratio
        #     rps_list = rps.tolist()
        #     rps_period.append(rps_list)
        #     # print(len(rps_list))
        rps_array = np.array(rps_period)
        # print(rps_array.shape)
        rps_array = rps_array.transpose(1, 0)
        return rps_array


if __name__ == '__main__':
    from base.pool.listed_time_pool import ListedTimePool
    pool_obj = ListedTimePool()
    pool = pool_obj.pool
    rps_calculator = RPS(250, 30, pool)
    rps_array = rps_calculator.rps_array
    print(rps_array.shape)
    print(rps_array[0])
    # price_ratio_array = rps_calculator.price_ratio_array
    # rps_result_list = []
    # for i, stock in enumerate(pool):
    #     df_need = np.array(stock[['ts_code']])
    #     ts_code = df_need[0][0]
    #     rps_result = str(ts_code) + ' ' + str(price_ratio_array[i]) + ' ' + str(rps_array[i])
    #     rps_result_list.append(rps_result)
    # rps_result_str = '\n'.join(rps_result_list)
    # rps_result_file = 'rps.txt'
    # with open(rps_result_file, 'w') as f:
    #     f.write(rps_result_str)
