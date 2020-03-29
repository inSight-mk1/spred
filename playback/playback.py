from tactics.daniel_tactics import DanielTactics
from tactics.uplimit_tactics import UplimitTactics
from multiprocessing import Pool
from tactics import config, config_dt


def part_pb(t_range):
    # print(t_range)
    win_cnt = 0
    all_cnt = 0
    bad_cnt = 0
    good_profit_cnt = 0
    total_profit = 0.0
    total_wr = 0.0
    total_gr = 0.0
    total_br = 0.0
    trade_t_cnt = 0
    for i in t_range:
        print(i)
        dt = None
        if config.playback_tactics == config.Daniel_tactics:
            dt = DanielTactics(t_before=i, play_back_mode=True)
        if config.playback_tactics == config.Uplimit_tactics:
            dt = UplimitTactics(t_before=i, play_back_mode=True)
        if dt is None:
            print("Platback_tactics is an unrecognized value. Please checkout config.py!")
        dt.select()
        res = dt.sell_point()
        t_win_cnt = 0
        t_bad_cnt = 0
        t_good_cnt = 0
        for r in res:
            if r >= 0.005:
                t_win_cnt += 1
                win_cnt += 1
                if r >= 0.10:
                    t_good_cnt += 1
                    good_profit_cnt += 1
            if r <= -0.07:
                t_bad_cnt += 1
                bad_cnt += 1
            all_cnt += 1
            total_profit += r
        sscnt = len(res)
        if sscnt > 0:
            single_wr = 1.0 * t_win_cnt / sscnt
            single_gr = 1.0 * t_good_cnt / sscnt
            single_br = 1.0 * t_bad_cnt / sscnt
            total_wr += single_wr
            total_gr += single_gr
            total_br += single_br
            trade_t_cnt += 1
            print("single_win_rate", single_wr)
    return win_cnt, all_cnt, good_profit_cnt, total_profit, bad_cnt, total_wr, total_gr, total_br, trade_t_cnt


class PlayBack(object):
    def __init__(self, pb_t=240, max_hold_t=config_dt.max_hold_t,
                 pb_t_start_from_now=None,
                 pb_t_end_from_now=None):
        self.pb_t = pb_t
        self.max_hold_t = max_hold_t
        self.pb_t_start_from_now = pb_t_start_from_now
        self.pb_t_end_from_now = pb_t_end_from_now

    def playback(self):

        pb_t_end = self.pb_t_end_from_now
        pb_t_start = self.pb_t_start_from_now

        if pb_t_end is not None and pb_t_start is not None and pb_t_start > pb_t_end and pb_t_end > self.max_hold_t:
            print("Valid range. Start playing back in selected time range.", pb_t_end, pb_t_start)
            start_t = pb_t_end  # self.pb_t_end means t-days FROM NOW, so start > end
            end_t = pb_t_start  # For our stock data struct(npArray), less index means nearer from now.
        else:
            print("Default playback mode. Time period", self.pb_t)
            start_t = self.max_hold_t + 1
            end_t = start_t + self.pb_t

        params = []
        all_t = range(start_t, end_t)
        splited_cnt = len(all_t) / config.nthreads + 1
        # print(splited_cnt)

        splited_t = [all_t[i:i + splited_cnt] for i in xrange(0, len(all_t), splited_cnt)]
        for st in splited_t:
            params.append(st)

        results = []
        pool = Pool(len(params))
        if config.multi_thread:
            results = pool.map(part_pb, params)
        else:
            results.append(part_pb(all_t))

        win_cnt = 0
        all_cnt = 0
        bad_cnt = 0
        good_profit_cnt = 0
        total_profit = 0.0
        e_weight_wr = 0.0
        e_weight_gr = 0.0
        e_weight_br = 0.0
        all_trade_t = 0
        for r in results:
            win_cnt += r[0]
            all_cnt += r[1]
            good_profit_cnt += r[2]
            total_profit += r[3]
            bad_cnt += r[4]
            e_weight_wr += r[5]
            e_weight_gr += r[6]
            e_weight_br += r[7]
            all_trade_t += r[8]

        # for i in range(start_t, end_t):
        #     print(i)
        #     dt = DanielTactics(t_before=i, max_hold_t=self.max_hold_t, play_back_mode=True)
        #     dt.select()
        #     res = dt.sell_point()
        #     for r in res:
        #         if r >= 0.005:
        #             win_cnt += 1
        #             if r > 0.10:
        #                 good_profit_cnt += 1
        #         all_cnt += 1
        #         total_profit += r

        good_profit_cnt = 1.0 * good_profit_cnt / all_cnt
        win_ratio = 1.0 * win_cnt / all_cnt
        bad_ratio = 1.0 * bad_cnt / all_cnt
        avg_profit = total_profit / all_cnt
        avg_cnt = 1.0 * all_cnt / self.pb_t
        e_weight_wr /= all_trade_t
        e_weight_gr /= all_trade_t
        e_weight_br /= all_trade_t
        return good_profit_cnt, win_ratio, avg_profit, bad_ratio, avg_cnt, e_weight_wr, e_weight_gr, e_weight_br


if __name__ == "__main__":
    # pb = PlayBack(pb_t_start_from_now=720,
    #               pb_t_end_from_now=340)
    pb = PlayBack(pb_t=630)
    gpr, wr, ap, br, avg_cnt, ewr, egr, ebr = pb.playback()

    print("good_rate", gpr, egr)
    print("win_rate", wr, ewr)
    print("bad_rate", br, ebr)
    print("ap", ap)
    print("avg_cnt", avg_cnt)

