import config
import config_dt
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

# This tactics is from https://www.youtube.com/watch?v=LT9U7O3joOY
# Thanks to Daniel
class DanielTactics(object):
    def __init__(self, new_high1=config_dt.new_high1, close_high_ratio=config_dt.close_high_ratio,
                 ma1=config_dt.ma1, ma2=config_dt.ma2,
                 week_ma1=config_dt.week_ma1, week_ma2=config_dt.week_ma2,
                 avg_amount_period=config_dt.avg_amount_period, large_amount_ratio=config_dt.large_amount_ratio,
                 ma_ratio=config_dt.ma_ratio, wma_ratio=config_dt.wma_ratio,
                 t_before=0, max_hold_t=config_dt.max_hold_t,
                 sell_below_ma=config_dt.sell_below_ma, loss_stop_pct=config_dt.loss_stop_pct,
                 up_ratio_low=config_dt.up_ratio_low, up_ratio_high=config_dt.up_ratio_high,
                 play_back_mode=False):
        self.new_high1 = new_high1
        self.close_high_ratio = close_high_ratio
        self.ma1 = ma1
        self.ma2 = ma2
        self.week_ma1 = week_ma1
        self.week_ma2 = week_ma2
        self.avg_amount_period = avg_amount_period
        self.large_amount_ratio = large_amount_ratio
        self.ma_ratio = ma_ratio
        self.wma_ratio = wma_ratio
        self.t_before = t_before
        self.max_hold_t = max_hold_t
        self.sell_below_ma = sell_below_ma
        self.loss_stop_pct = loss_stop_pct
        self.play_back_mode = play_back_mode
        self.up_ratio_low = up_ratio_low
        self.up_ratio_high = up_ratio_high

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

            last_amount = df_need[1][4]
            # print(df[0])
            # Get ma1 (default = 20)
            # current_ma1 = 0.0
            # for i in range(self.ma1):
            #     current_ma1 += df_need[i][3]
            # current_ma1 /= self.ma1
            current_ma1 = np.mean(df_need[0:self.ma1, 3])

            # Get ma2 (default = 60)
            # current_ma2 = 0.0
            # for i in range(self.ma2):
            #     current_ma2 += df_need[i][3]
            # current_ma2 /= self.ma2
            current_ma2 = np.mean(df_need[0:self.ma2, 3])

            # Get modified week ma1
            # current_wma1 = 0.0
            # end_idx = self.week_ma1 * 5
            # for i in range(0, end_idx, 5):
            #     current_wma1 += df_need[i][3]
            # current_wma1 /= self.week_ma1
            #
            # # Get modified week ma2
            # current_wma2 = 0.0
            # end_idx = self.week_ma2 * 5
            # for i in range(0, end_idx, 5):
            #     current_wma2 += df_need[i][3]
            # current_wma2 /= self.week_ma2
            #
            # print(current_ma1, current_ma2, current_wma1, current_wma2)

            # Get avg amount
            # current_avg_amount = 0.0
            # for i in range(self.avg_amount_period):
            #     current_avg_amount += df_need[i][4]
            # current_avg_amount /= self.avg_amount_period
            current_avg_amount = np.mean(df_need[1:self.avg_amount_period+1, 4])

            # Get max1
            current_max1 = 0.0
            for i in range(self.new_high1):
                high_p = df_need[i][1]
                if high_p > current_max1:
                    current_max1 = high_p

            # Start to judge if this stock is suitable for buying

            current_close = df_need[0][3]
            current_high = df_need[0][1]
            current_amount = df_need[0][4]
            current_ratio_from_high = (current_high - current_close) / current_close

            dist_ratio_to_ma1 = (current_close - current_ma1) / current_ma1
            dist_ratio_to_ma2 = (current_close - current_ma2) / current_ma2
            # dist_ratio_to_wma1 = (current_close - current_wma1) / current_wma1
            # dist_ratio_to_wma2 = (current_close - current_wma2) / current_wma2
            condition1 = (current_high >= current_max1)
            condition2 = current_ratio_from_high <= self.close_high_ratio
            condition3 = (current_amount >= current_avg_amount * self.large_amount_ratio)
            condition4 = (abs(dist_ratio_to_ma1) <= self.ma_ratio)
            condition5 = (0 <= dist_ratio_to_ma2 <= self.ma_ratio)
            # condition6 = (abs(dist_ratio_to_wma1) <= self.wma_ratio)
            # condition7 = (abs(dist_ratio_to_wma2) <= self.wma_ratio)

            condition8 = (self.up_ratio_high >= t_pct_chg >= self.up_ratio_low)

            # single test
            # if "600779" in stock_file:
            #     print(condition1)
            #     print(condition2)
            #     print(condition3)
            #     print(condition8)
            #     print(t_pct_chg)
            #     print(dist_ratio_to_ma1)
            #     print(dist_ratio_to_ma2)

            if condition1 and condition2 and condition3 and condition4 \
                    and condition8:
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
        random_selected = self.selected_stock
        # if len(self.selected_stock) > 3:
        #     random_selected = random.sample(self.selected_stock, 3)
        for stock_file in random_selected:
            df = pd.read_csv(stock_file)
            # 0:open, 1:high, 2:low, 3:close, 4:amount
            df_need = np.array(df[['open', 'high', 'low', 'close', 'amount',
                                   'trade_date']])
            buy_price = df_need[self.t_before - 1][0]
            buy_day = df_need[self.t_before - 1][5]
            before_buy_low = df_need[self.t_before][0]
            early_sell = False
            sell_day = None
            half_sell = False

            for t in range(1, self.max_hold_t):
                # print(self.max_hold_t)
                current_idx = self.t_before - 1 - t
                t_low = df_need[current_idx][2]
                t_close = df_need[current_idx][3]
                t_high = df_need[current_idx][1]

                # t_ma1 = t_low
                # for i in range(self.sell_below_ma - 1):
                #     t_ma1 += df_need[current_idx + i][3]
                # t_ma1 /= self.sell_below_ma
                t_ma1 = np.mean(df_need[current_idx:current_idx + self.sell_below_ma, 3])

                condition1 = (t_close < t_ma1) and (t_close >= buy_price)
                condition2 = (t_close < before_buy_low)
                condition3 = (t_close < buy_price * (1 - self.loss_stop_pct))
                condition4 = (t_high > buy_price)

                # If profit reaches 3%, sell half of stock

                if config_dt.half_sell_flag:
                    half_sell_price = buy_price * (1 + config_dt.half_sell_ratio)
                    if t_high >= half_sell_price:
                        half_sell = True

                if condition1 or condition2 or condition3:
                    # sell_price = 0.0
                    # if condition4:
                    #     sell_price = t_high * 0.99
                    # else:
                    #     sell_price = t_close
                    sell_price = t_close
                    if half_sell:
                        sell_price = (sell_price + half_sell_price) * 0.5
                    pct = (sell_price - buy_price) / buy_price
                    sell_day = df_need[current_idx][5]
                    print(stock_file, "%.4f" % pct, buy_day, "%.2f" % buy_price,
                          sell_day, "%.2f" % sell_price,
                          [condition1, condition2, condition3, half_sell])
                    selected_results.append(pct)
                    early_sell = True
                    break

            if not early_sell:
                last_day_close = df_need[self.t_before - self.max_hold_t][3]
                sell_day = df_need[self.t_before - self.max_hold_t][5]
                pct = (last_day_close - buy_price) / buy_price
                print(stock_file, "%.4f" % pct, buy_day, "%.2f" % buy_price,
                          sell_day, "%.2f" % last_day_close, "Max_hold_t reached!")
                selected_results.append(pct)

        return selected_results
