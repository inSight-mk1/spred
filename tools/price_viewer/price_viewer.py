from tools.price_viewer.price_grabber import Price_Grabber
from prettytable import PrettyTable
import time
from tools.time_domain_list import TimeDomainList

if __name__ == '__main__':
    pg = Price_Grabber()
    stock_list = []
    with open('stock_list.txt', 'r') as f:
        lines = f.readlines()
        for line in lines:
            stock_code = line.strip()
            stock_list.append(stock_code)
    print(stock_list)
    stock_tdl = []
    for stock_code in stock_list:
        tdl = TimeDomainList(element_cnt=12)
        stock_tdl.append(tdl)
    main_table = PrettyTable(['stock_code', 'stock_name', 'current_price', 'current_ratio', 'volatility', 'time', 'date'])

    while(True):
        current_table = main_table[:]
        for i, stock_code in enumerate(stock_list):
            res = pg.grab(stock_code)
            stock_tdl[i].push(float(res['ratio'][:-1]))
            volatility_s = ''
            if stock_tdl[i].list[0] is not None:
                volatility_ratio = stock_tdl[i].list[-1] - stock_tdl[i].list[0]
                volatility_s = "%.2f%%" % volatility_ratio
            current_table.add_row([stock_code, res['stock_name'], res['current_price'], res['ratio'], volatility_s,
                                   res['current_time'], res['current_date']])
        print(time.strftime('%H:%M:%S', time.localtime(time.time())))
        print(current_table)
        time.sleep(10)
