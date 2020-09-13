from config import config_private as config
import pandas as pd
import os
import numpy as np


def load_data(path):
    # print path
    list_path = os.path.join(path, 'all_list.txt')
    paths = []
    with open(list_path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.replace('\n', '')
            paths.append(line)

        print('There are {} pieces of data in txt file'.format((len(paths))))

    stocks_data = []
    for path in paths:
        df = pd.read_csv(path)
        stocks_data.append(df)

    for i in range(len(stocks_data)):
        stocks_data[i]['idx'] = i
        stocks_data[i].rename(columns={'Unnamed: 0': 'time_idx'}, inplace=True)

    return stocks_data


class StockPool(object):
    def __init__(self, data_path=config.save_path):
        self.all_data = load_data(data_path)
        self.pool = None  # returns none in father class

    def get_price(self, stock_idx, time_idx, ptype='open'):
        df_need = np.array(self.all_data[stock_idx][ptype])
        return df_need[time_idx]
