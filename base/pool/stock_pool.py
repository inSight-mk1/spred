from config import config_private as config
import pandas as pd
import os


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
    for data_path in paths:
        df = pd.read_csv(data_path)
        stocks_data.append(df)

    return stocks_data


class StockPool(object):
    def __init__(self, data_path=config.save_path):
        self.all_data = load_data(data_path)
        self.pool = None  # returns none in father class
