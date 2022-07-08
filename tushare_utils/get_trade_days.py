import tushare as ts
import numpy as np
from config import config_private as cfgp


def get_trade_days(start_date, end_date):
    my_token = cfgp.my_token
    ts.set_token(my_token)
    ts_api = ts.pro_api()
    df = ts_api.trade_cal(exchange='', start_date=start_date, end_date=end_date)
    cal_date = np.array(df['cal_date'])
    trade_status = np.array(df['is_open'])

    trade_days = []
    for i, status in enumerate(trade_status):
        if status == 1:
            trade_days.append(cal_date[i])
    return trade_days


if __name__ == '__main__':
    print(get_trade_days('20220501', '20220707'))