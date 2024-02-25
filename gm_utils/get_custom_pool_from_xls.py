# coding=utf-8
import pandas as pd
from tqdm import tqdm


def get_custom_pool_from_xls(xls_file):
    pool = pd.read_excel(xls_file, sheet_name="Sheet1", usecols="A:G")
    pool_null = pool.isnull()
    data_len = len(pool['symbol'])
    concepts = []
    pool_by_concept_everyday = {}
    m_value_everyday = {}
    ratio_everyday = {}
    open_ratio_everyday = {}
    for i in range(0, data_len):
        symbol = pool['symbol'][i]
        if not pool_null['symbol'][i] and len(symbol) > 1:
            current_date = pool['date'][i]
            yr, mon, day = current_date.split('-')[0].split('.')
            mon = mon.zfill(2)  # '3' -> '03'
            day = day.zfill(2)  # '3' -> '03'
            current_date = '20%s-%s-%s' % (yr, mon, day)
            if current_date not in pool_by_concept_everyday.keys():
                pool_by_concept_everyday[current_date] = []
                concepts.clear()
                m_value_everyday[current_date] = []
                ratio_everyday[current_date] = []
                open_ratio_everyday[current_date] = []

            m_value = pool['m_value'][i]
            ratio = pool['lastd_ratio'][i]
            open_ratio = pool['open_ratio'][i]
            try:
                ratio = float(ratio.strip('%'))
            except:
                ratio = ratio * 100
            try:
                open_ratio = float(open_ratio.strip('%'))
            except:
                open_ratio = open_ratio * 100

            concept = pool['concept'][i]
            if concept in concepts:
                con_idx = concepts.index(concept)
                pool_by_concept_everyday[current_date][con_idx].append(symbol)
                m_value_everyday[current_date][con_idx].append(m_value)
                ratio_everyday[current_date][con_idx].append(ratio)
                open_ratio_everyday[current_date][con_idx].append(open_ratio)
            else:
                concepts.append(concept)
                pool_by_concept_everyday[current_date].append([symbol])
                m_value_everyday[current_date].append([m_value])
                ratio_everyday[current_date].append([ratio])
                open_ratio_everyday[current_date].append([open_ratio])

    pool_allinfo_everyday = {}
    for date in pool_by_concept_everyday.keys():
        pool_by_concept = pool_by_concept_everyday[date]
        m_value_by_concept = m_value_everyday[date]
        ratio_by_concept = ratio_everyday[date]
        open_ratio_by_concept = open_ratio_everyday[date]
        info_tuple = (pool_by_concept, m_value_by_concept, ratio_by_concept, open_ratio_by_concept)
        pool_allinfo_everyday[date] = info_tuple

    return pool_allinfo_everyday


if __name__ == '__main__':
    file_path = "stock_pool_23.2_full_v2.xls"
    print(get_custom_pool_from_xls(file_path))
