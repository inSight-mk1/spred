import os
import torch
from torch.utils.data import Dataset, DataLoader
import config
import pandas as pd
import numpy as np
import random


class StockDataset(Dataset):
    def __init__(self, data_path, train_flag, window=config.window_size):
        self.data_path = data_path
        self.train_flag = train_flag
        self.data_sets = self.load_data()
        self.window = window

    def __len__(self):
        return len(self.data_sets)

    def __getitem__(self, item):
        single_path = self.data_sets[item]
        df = pd.read_csv(single_path)

        # All columes below:
        # ts_code    trade_date   open            high       low           close
        # pre_close  change       pct_chg         vol        amount
        # We NEED below:
        # open high low close pct_chg amount

        df_need = np.array(df[['open', 'high', 'low', 'close', 'amount']])
        ridx = random.randint(config.pred_time[-1] + 20, len(df_need) - self.window)
        # print(ridx)

        # window_data: from late to early, e.g. 20190628 - 20190428
        window_data = df_need[ridx:ridx+self.window]

        # Convert all data to change_rate of the last day close, so is amount
        last_close = window_data[0][3]
        last_amount = window_data[0][4]

        for i in range(self.window):
            # e.g if last day's close is 7.98, one day's open is 10.01, then data = 10.01 / 7.98
            window_data[i][0] /= last_close
            window_data[i][1] /= last_close
            window_data[i][2] /= last_close
            window_data[i][3] /= last_close
            window_data[i][4] /= last_amount

        # label = []

        lidx = ridx - config.pred_time[0]
        t_close = last_close
        tplus_close = df_need[lidx][3]
        pct_chg = tplus_close / t_close

        # one_hot = np.zeros((len(config.cls)), dtype=np.int64)

        label = 0
        for i in range(len(config.cls)):
            if i == 0:
                if (pct_chg - 1.0) >= config.cls[i]:
                    # one_hot[i] = 1
                    label = i
                    break
            else:
                if config.cls[i - 1] > (pct_chg - 1.0) >= config.cls[i]:
                    # one_hot[i] = 1
                    label = i
                    break

            # if t_pct_chg > 0:
            #     label.append(1.0)
            # else:
            #     label.append(0.0)

        # label = one_hot

        label = np.array(label)

        return {'window': window_data.astype(np.float32), 'label': label.astype(np.float32)}

    def load_data(self):
        path = self.data_path
        if self.train_flag:
            path = os.path.join(path, 'train_list.txt')
        else:
            path = os.path.join(path, 'test_list.txt')

        print path

        with open(path, 'r') as f:
            lines = f.readlines()
            single_paths = []
            for line in lines:
                line = line.replace('\n', '')
                single_paths.append(line)

            print('There are {} pieces of data in txt file'.format((len(single_paths))))

            return single_paths

