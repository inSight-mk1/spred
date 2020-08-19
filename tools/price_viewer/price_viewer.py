from tools.price_viewer.price_grabber import Price_Grabber
from prettytable import PrettyTable
import time

if __name__ == '__main__':
    pg = Price_Grabber()
    stock_list = []
    with open('stock_list.txt', 'r') as f:
        lines = f.readlines()
        for line in lines:
            stock_code = line.strip()
            stock_list.append(stock_code)
    print(stock_list)
    table = PrettyTable(['stock_code', 'stock_name', 'current_price', 'current_ratio', 'time', 'date'])
    while(True):
        current_table = table[:]
        for stock_code in stock_list:
            res = pg.grab(stock_code)
            current_table.add_row([stock_code, res['stock_name'], res['current_price'], res['ratio'],
                                   res['current_time'], res['current_date']])
        print(current_table)
        time.sleep(10)
