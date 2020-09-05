import os
import pandas as pd
import numpy as np
from config import config_private as config


class MAAcquirer(object):
    def __init__(self, ts_code, ma=10):
        self.ts_code = ts_code
        self.ma = ma
        self.stock_data_path = os.path.join(config.save_path, ts_code + '.csv')
        self.df = pd.read_csv(self.stock_data_path)
        self.price_ma = None
        self.current_price = None

    def acquire_ma(self, ma=None):
        # 0:open, 1:high, 2:low, 3:close, 4:amount
        df_need = np.array(self.df[['open', 'high', 'low', 'close', 'amount',
                                    'trade_date', 'pct_chg']])
        if ma is not None:
            self.ma = ma
        self.price_ma = np.mean(df_need[0:self.ma, 3])
        self.current_price = df_need[0, 3]
        return self.price_ma


if __name__ == '__main__':
    # Test
    maa = MAAcquirer(ts_code='300745.SZ', ma=8)
    print(maa.acquire_ma())
