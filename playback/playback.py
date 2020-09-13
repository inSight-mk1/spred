from tactics.rps_tactics import RPSTactics
from base.pool.stock_pool import StockPool


class PlayBack(object):
    def __init__(self, pb_t=250):
        self.pb_t = pb_t

    def playback(self):
        reused_pool = StockPool()
        playback_t = self.pb_t
        hold_list = []
        win_cnt = 0
        total_cnt = 0
        total_profit = 0
        hold_cnt = 2
        init_hold_value = 1.0 / hold_cnt
        last_selected = []
        init_value = 1.0
        for t in range(playback_t, -1, -1):
            print(t)
            tactics = RPSTactics(reused_pool=reused_pool, t=t, rps_n=250, thresh_min=90, thresh_max=93,
                                 new_high_t=20, hold_cnt=hold_cnt, sold_ma=20, hold_value=init_hold_value)
            tactics.hold_list = hold_list
            sold_list, profits = tactics.sold()
            for profit in profits:
                if profit >= 0.002:
                    win_cnt += 1
                total_profit += profit
            total_cnt += len(profits)
            current_hold_cnt = len(tactics.hold_list)
            target_hold_cnt = tactics.hold_cnt
            buy_cnt = target_hold_cnt - current_hold_cnt
            selected_list = tactics.select(select_cnt=buy_cnt)
            tactics.buy(selected_list)
            hold_list = tactics.hold_list
            if t == playback_t:
                print('value', init_value)
                last_selected = selected_list
                continue

            if total_cnt > 0:
                print('win_rate =', win_cnt / total_cnt)
                print('average_profit =', total_profit / total_cnt)

            total_value = 0
            for stock in sold_list:
                stock_idx = stock['stock_idx']
                time_idx = t
                pct_chg = reused_pool.get_price(stock_idx, time_idx, 'pct_chg')
                ratio = 1 + pct_chg * 0.01
                returned_value = stock['hold_value'] * ratio
                total_value += returned_value
            if len(sold_list) > 0:
                # TODO: Set hold_value before selecting
                init_hold_value = total_value / len(sold_list)

            print('Calculating realtime value')
            print(last_selected)
            for i, stock in enumerate(hold_list):
                if stock in selected_list:
                    continue
                # print(stock)
                if stock in last_selected:
                    stock_idx = stock['stock_idx']
                    time_idx = t
                    open_price = reused_pool.get_price(stock_idx, time_idx, 'open')
                    close_price = reused_pool.get_price(stock_idx, time_idx, 'close')
                    open_close_ratio = close_price / open_price
                    hold_list[i]['hold_value'] *= open_close_ratio
                    # print(open_close_ratio, hold_list[i]['hold_value'])
                else:
                    stock_idx = stock['stock_idx']
                    time_idx = t
                    pct_chg = reused_pool.get_price(stock_idx, time_idx, 'pct_chg')
                    ratio = 1 + pct_chg * 0.01
                    hold_list[i]['hold_value'] *= ratio
                total_value += hold_list[i]['hold_value']
            print('value', total_value)
            last_selected = selected_list


if __name__ == "__main__":
    # pb = PlayBack(pb_t_start_from_now=720,
    #               pb_t_end_from_now=340)
    pb = PlayBack(pb_t=250)
    pb.playback()
