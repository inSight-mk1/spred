import config
import config_xt
import pandas as pd
import numpy as np
import random


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


class XXNBTactics(object):
    def __init__(self, high_range=config_xt.high_range, high_dist_range=config_xt.high_dist_range,
                 gap_dist_range=config_xt.gap_dist_range, shock_ratio=config_xt.shock_ratio,
                 gap_up_ratio=config_xt.gap_up_ratio, box_mode=config_xt.box_mode, play_back_mode=False, t_before=0):
        self.high_range = high_range
        self.high_dist_range = high_dist_range
        self.gap_dist_range = gap_dist_range
        self.shock_ratio_thres = shock_ratio
        self.box_mode = box_mode
        self.gap_up_ratio = gap_up_ratio
        self.play_back_mode = play_back_mode
        self.t_before = t_before

        self.selected_stock = []

    def select(self):
        selected = []
        stock_list = load_data(config.data_path)
        for stock_file in stock_list:
            df = pd.read_csv(stock_file)
            df = df[self.t_before:]

            # 0:open, 1:high, 2:low, 3:close, 4:amount
            df_need = np.array(df[['open', 'high', 'low', 'close', 'amount',
                                   'trade_date', 'pct_chg']])
            # print(df_need.shape)

            t_pct_chg = df_need[0][6]

            # 1. close to ma20 or ma50
            current_ma1 = np.mean(df_need[0:config_xt.ma1, 3])
            current_close = df_need[0][3]
            dist_ratio = abs(current_close - current_ma1) / current_close
            # print(current_ma1, current_close, dist_ratio)
            if (dist_ratio > config_xt.ma_dist_ratio):
                continue

            # 2. Find gap
            nogap = True
            for i in config_xt.gap_search_range:
                t_low = df_need[i][2]
                t1_high = df_need[i + 1][1]
                if t_low > t1_high: # Check if gap has been filled
                    nogap = False
                    for j in range(i):
                        if df_need[j][2] <= t1_high:
                            nogap = True
                            break
                    # Check if publish fin-report

            if (nogap):
                continue
            # # Get max1
            # current_max1 = 0.0
            # high_t = -1
            # for i in range(self.high_dist_range[0], self.high_range):
            #     if self.box_mode == config_xt.BOX_HIGH_MODE:
            #         high_p = df_need[i][1]
            #     else:
            #         high_p = df_need[i][3]
            #     if high_p > current_max1:
            #         current_max1 = high_p
            #         high_t = i
            #
            # # High point not in range
            # if high_t > self.high_dist_range[1]:
            #     continue
            #
            # gap = False
            # upLimit = False
            # for i in range(high_t + 1, high_t + 1 + self.gap_dist_range):
            #     if df_need[i][6] >= 9.9:
            #         upLimit = True
            #         break
            #     if df_need[i][2] > df_need[i+1][1] and df_need[i][6] >= self.gap_up_ratio:
            #         gap = True
            #         break
            #
            # # No gap and uplimit
            # if not (gap):
            #     continue
            #
            # shock_max = 0.0
            # shock_min = 9999.99
            # for i in range(high_t + 1):
            #     if df_need[i][1] > shock_max:
            #         shock_max = df_need[i][1]
            #     if df_need[i][2] < shock_min:
            #         shock_min = df_need[i][2]
            #
            # shock_range = shock_max - shock_min
            # shock_ratio = shock_range / shock_min
            # # print(shock_max, shock_min, shock_ratio)
            # if shock_ratio > self.shock_ratio_thres:
            #     continue

            if not self.play_back_mode:
                print(stock_file, df_need[0][5])
            selected.append(stock_file)

        self.selected_stock = selected
        if not self.play_back_mode:
            print(len(selected))
        return selected

    # def sell_point(self):
    #     if self.t_before < self.max_hold_t:
    #         print ("t_before < max_hold_t ! History test failed! Please set t_before correctly!")
    #         return None
    #     selected_results = []
    #     # if len(self.selected_stock) == 1:
    #     #     self.sell_below_ma = 5
    #     # if 1 < len(self.selected_stock) <= 3:
    #     #     self.sell_below_ma = 10
    #     random_selected = self.selected_stock
    #     # if len(self.selected_stock) > 3:
    #     #     random_selected = random.sample(self.selected_stock, 3)
    #     for stock_file in random_selected:
    #         df = pd.read_csv(stock_file)
    #         # 0:open, 1:high, 2:low, 3:close, 4:amount
    #         df_need = np.array(df[['open', 'high', 'low', 'close', 'amount',
    #                                'trade_date']])
    #         buy_price = df_need[self.t_before - 1][0]
    #         buy_day = df_need[self.t_before - 1][5]
    #         before_buy_low = df_need[self.t_before][2]
    #         early_sell = False
    #         sell_day = None
    #         half_sell = False
    #
    #         for t in range(1, self.max_hold_t):
    #             # print(self.max_hold_t)
    #             current_idx = self.t_before - 1 - t
    #             t_low = df_need[current_idx][2]
    #             t_close = df_need[current_idx][3]
    #             t_high = df_need[current_idx][1]
    #
    #             # t_ma1 = t_low
    #             # for i in range(self.sell_below_ma - 1):
    #             #     t_ma1 += df_need[current_idx + i][3]
    #             # t_ma1 /= self.sell_below_ma
    #             t_ma1 = np.mean(df_need[current_idx:current_idx + self.sell_below_ma, 3])
    #
    #             condition1 = (t_close < t_ma1)
    #             condition2 = (t_close < before_buy_low)
    #             condition3 = (t_close < buy_price * (1 - self.loss_stop_pct))
    #             condition4 = (t_high > buy_price)
    #
    #             # If profit reaches 3%, sell half of stock
    #             half_sell_price = buy_price * 1.03
    #             if t_high >= half_sell_price:
    #                 half_sell = True
    #
    #             if condition1 or condition2 or condition3:
    #                 # sell_price = 0.0
    #                 # if condition4:
    #                 #     sell_price = t_high * 0.99
    #                 # else:
    #                 #     sell_price = t_close
    #                 sell_price = t_close
    #                 if half_sell:
    #                     sell_price = (sell_price + half_sell_price) * 0.5
    #                 pct = (sell_price - buy_price) / buy_price
    #                 sell_day = df_need[current_idx][5]
    #                 print(stock_file, "%.4f" % pct, buy_day, "%.2f" % buy_price,
    #                       sell_day, "%.2f" % sell_price,
    #                       [condition1, condition2, condition3, half_sell])
    #                 selected_results.append(pct)
    #                 early_sell = True
    #                 break
    #
    #         if not early_sell:
    #             last_day_close = df_need[self.t_before - self.max_hold_t][3]
    #             sell_day = df_need[self.t_before - self.max_hold_t][5]
    #             pct = (last_day_close - buy_price) / buy_price
    #             print(stock_file, "%.4f" % pct, buy_day, "%.2f" % buy_price,
    #                       sell_day, "%.2f" % last_day_close, "Max_hold_t reached!")
    #             selected_results.append(pct)
    #
    #     return selected_results
