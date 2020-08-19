import requests


class Price_Grabber(object):
    def __init__(self):
        self.interface_url = 'http://hq.sinajs.cn/list='

    def grab(self, stock_code):
        url = self.interface_url + stock_code
        r = requests.get(url)
        return self.parse_text(r.text)

    def parse_text(self, text: str):
        left_start_idx = text.index('="') + 2
        info_text = text[left_start_idx:]
        s_texts = info_text.split(',')
        last_day_price_f = float(s_texts[2])
        current_price_f = float(s_texts[3])
        ratio = (current_price_f - last_day_price_f) / last_day_price_f * 100
        ratio_s = '%.2f%%' % ratio
        return dict(stock_name=s_texts[0], ratio=ratio_s, current_price=s_texts[3], current_date=s_texts[30], current_time=s_texts[31])


if __name__ == '__main__':
    pg = Price_Grabber()
    print(pg.grab('sh601006'))
