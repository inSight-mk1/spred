import config
import config_ut
import pandas as pd
import numpy as np


def load_data(path):
    # print path

    with open(path, 'r') as f:
        lines = f.readlines()
        single_paths = []
        for line in lines:
            line = line.replace('\n', '')
            single_paths.append(line)

        # print('There are {} pieces of data in txt file'.format((len(single_paths))))

        return single_paths


class UplimitTactics(object):
    def __init__(self, uplimit_ratio=0.099,
                 t_before=0, max_hold_t=10,
                 open_pct_chg_thres=config_ut.open_pct_chg_thres,
                 sell_below_ma=config_ut.sell_below_ma,
                 loss_stop_pct=config_ut.loss_stop_pct,
                 profit_stop_pct=config_ut.profit_stop_pct,
                 play_back_mode=False):
        self.uplimit_ratio = uplimit_ratio * 100.0
        self.play_back_mode = play_back_mode
        self.max_hold_t = max_hold_t
        self.t_before = t_before
        self.open_pct_chg_thres = open_pct_chg_thres
        self.sell_below_ma = sell_below_ma
        self.loss_stop_pct = loss_stop_pct
        self.profit_stop_pct = profit_stop_pct

        self.selected_stock = []

    def select(self):

        selected = []
        stock_list = load_data(config.data_path)
        for stock_file in stock_list:
            df = pd.read_csv(stock_file)
            df = df[self.t_before:]

            # 0:open, 1:high, 2:low, 3:close, 4:pct_chg
            df_need = np.array(df[['open', 'high', 'low', 'close', 'pct_chg',
                                   'trade_date']])

            t_pct_chg = df_need[0][4]

            condition1 = t_pct_chg >= self.uplimit_ratio

            if condition1:
                if not self.play_back_mode:
                    print(stock_file, df_need[0][5])
                selected.append(stock_file)

        self.selected_stock = selected
        if not self.play_back_mode:
            print(len(selected))
        return selected

    def sell_point(self):
        if self.t_before < self.max_hold_t:
            print ("t_before < max_hold_t ! History test failed! Please set t_before correctly!")
            return None
        selected_results = []
        # if len(self.selected_stock) == 1:
        #     self.sell_below_ma = 5
        # if 1 < len(self.selected_stock) <= 3:
        #     self.sell_below_ma = 10
        for stock_file in self.selected_stock:
            df = pd.read_csv(stock_file)
            # 0:open, 1:high, 2:low, 3:close, 4:amount
            df_need = np.array(df[['open', 'high', 'low', 'close', 'amount',
                                   'trade_date']])
            last_day_close = df_need[self.t_before][3]  # select_day_close
            buy_price = df_need[self.t_before - 1][0]
            buy_pct = (buy_price - last_day_close) / last_day_close
            if buy_pct > self.open_pct_chg_thres:
                continue

            buy_price = df_need[self.t_before - 1][0]
            buy_day = df_need[self.t_before - 1][5]
            before_buy_low = df_need[self.t_before][2]
            early_sell = False
            sell_day = None
            half_sell = False
            profit_stop_price = buy_price * (1 + self.profit_stop_pct)
            loss_stop_price = buy_price * (1 - self.loss_stop_pct)

            for t in range(1, self.max_hold_t):
                # t_before: select_day; t_before - 1: buy_day; t: hold_time
                current_idx = self.t_before - 1 - t
                t_low = df_need[current_idx][2]
                t_close = df_need[current_idx][3]
                t_high = df_need[current_idx][1]

                # t_ma1 = t_low
                # for i in range(self.sell_below_ma - 1):
                #     t_ma1 += df_need[current_idx + i][3]
                # t_ma1 /= self.sell_below_ma

                # print(df_need[current_idx:current_idx+self.sell_below_ma, 3])
                t_ma1 = np.mean(df_need[current_idx:current_idx+self.sell_below_ma, 3])

                condition1 = (t_close < t_ma1)
                condition2 = (t_high >= profit_stop_price)
                condition3 = (t_low <= loss_stop_price)
                # condition4 = (t_high > buy_price)

                # If profit reaches 3%, sell half of stock
                # half_sell_price = buy_price * 1.03
                # if t_high >= half_sell_price:
                #     half_sell = True

                if condition1 or condition2 or condition3:
                    # sell_price = 0.0
                    # if condition4:
                    #     sell_price = t_high * 0.99
                    # else:
                    #     sell_price = t_close
                    sell_price = t_close
                    if condition2:
                        sell_price = profit_stop_price
                    if condition3:
                        sell_price = loss_stop_price
                    # if half_sell:
                    #     sell_price = (sell_price + half_sell_price) * 0.5
                    pct = (sell_price - buy_price) / buy_price
                    sell_day = df_need[current_idx][5]
                    print(stock_file, "%.4f" % pct, buy_day, "%.2f" % buy_price,
                          sell_day, "%.2f" % sell_price,
                          [condition1, condition2, condition3])
                    selected_results.append(pct)
                    early_sell = True
                    break

            if not early_sell:
                last_day_close = df_need[self.t_before - self.max_hold_t][3]
                pct = (last_day_close - buy_price) / buy_price
                print(stock_file, pct, "max_hold")
                selected_results.append(pct)

        return selected_results
