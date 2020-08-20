from tools.price_viewer.price_grabber import Price_Grabber
from prettytable import PrettyTable
import time
from tools.time_domain_list import TimeDomainList

if __name__ == '__main__':
    pg = Price_Grabber()
    stock_list = []
    hold_count_list = []
    with open('stock_list.txt', 'r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            stock_code = line
            stock_list.append(stock_code)
    print(stock_list)
    stock_tdl = []
    for stock_code in stock_list:
        tdl = TimeDomainList(element_cnt=12)
        stock_tdl.append(tdl)
    main_table = PrettyTable(['stock_code', ' stock_name ', ' price ', ' ratio ', 'volatility',
                              'today_low', 'today_high', 'time'])

    while(True):
        current_table = main_table[:]
        for i, stock_code in enumerate(stock_list):
            res = pg.grab(stock_code)
            stock_tdl[i].push(float(res['ratio'][:-1]))
            volatility_s = ''
            if stock_tdl[i].list[0] is not None:
                volatility_ratio = stock_tdl[i].list[-1] - stock_tdl[i].list[0]
                if volatility_ratio > 0:
                    volatility_ratio = stock_tdl[i].list[-1] - min(stock_tdl[i].list)
                else:
                    volatility_ratio = stock_tdl[i].list[-1] - max(stock_tdl[i].list)
                volatility_s = "%.2f%%" % volatility_ratio
            current_table.add_row([stock_code, res['stock_name'],
                                   res['current_price'], res['ratio'], volatility_s,
                                   res['today_low'], res['today_high'], res['current_time']])
        print(time.strftime('%H:%M:%S', time.localtime(time.time())))
        current_table.align = "r"
        # current_table.set_style(MARKDOWN)
        print(current_table.get_string(sortby=" ratio "))
        time.sleep(10)
