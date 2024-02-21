# coding=utf-8
import pandas as pd
from tqdm import tqdm


def get_custom_pool_from_xls(xls_file):
    pool = pd.read_excel(xls_file, sheet_name="Sheet1", usecols="A:F")
    pool_null = pool.isnull()
    data_len = len(pool['symbol'])
    concepts = []
    pool_by_concept_everyday = {}
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

            concept = pool['concept'][i]
            if concept in concepts:
                con_idx = concepts.index(concept)
                pool_by_concept_everyday[current_date][con_idx].append(symbol)
            else:
                concepts.append(concept)
                pool_by_concept_everyday[current_date].append([symbol])

    return pool_by_concept_everyday


if __name__ == '__main__':
    file_path = "stock_pool_full.xls"
    print(get_custom_pool_from_xls(file_path))
