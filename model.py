import json
import os

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt


def summarize_data(root, out, term='tacoma'):
    dct = {}
    ct = 0
    _files = [os.path.join(root, x) for x in os.listdir(root) if term.lower() in x]
    od_ct = 0
    for f in _files:
        with open(f, 'r') as f_:
            file_obj = json.load(f_)
        file_obj = [v for k, v in file_obj.items()][0]
        for city, d in file_obj.items():
            if len(d.keys()) > 0:
                ct += len(d.keys())
                for k, v in d.items():
                    if term.lower() not in k.lower():
                        continue
                    basename = os.path.basename(v['url']).split('.')[0]
                    try:
                        odom = float(v['odometer'])
                        od_ct += 1
                        if odom < 5000 or odom > 300000:
                            continue
                        if v['drive'] != '4wd':
                            continue
                        dct[basename] = {'price': v['price'],
                                         'year': v['year'],
                                         'odometer': v['odometer'],
                                         'url': v['url']}

                    except (ValueError, TypeError):
                        continue

    print('{} complete records'.format(od_ct))
    with open(out, 'w') as _f:
        json.dump(dct, _f, indent=4)


def model(records, csv):
    with open(records, 'r') as _f:
        dct = json.load(_f)
    err, ct = 0, -1
    cols = ['code', 'year', 'odometer', 'price_list', 'price_pred', 'url']
    df = pd.DataFrame(data=None, columns=cols)
    for k, v in dct.items():
        try:
            price = float(v['price'])
            if price < 1000:
                continue
            odom, year = float(v['odometer']), float(v['year'])
            url = v['url']
            ct += 1
            df.loc[ct] = {'code': k, 'year': year, 'odometer': odom, 'price_list': price,
                          'price_pred': None, 'diff': None, 'url': url}
        except ValueError:
            err += 1

    y = df['price_list'].values
    x = df['odometer'].values.reshape(-1, 1)
    ulr = LinearRegression()
    ulr.fit(x, y)

    x = df[['year', 'odometer']].values
    x[:, 0] = 2023 - x[:, 0]
    mlr = LinearRegression()
    mlr.fit(x, y)
    y_pred = mlr.predict(x)
    res = (y - y_pred) / y

    df['price_list'] = y.astype(int)
    df['price_pred'] = y_pred.astype(int)
    df = df[cols]
    df['diff'] = res
    df = df.sort_values('diff')
    df.to_csv(csv, float_format='%.2f')


if __name__ == '__main__':
    d = '/home/dgketchum/PycharmProjects/CraigslistScraper/data'
    data = os.path.join(d, '30-Jan-2023')

    truck = 'frontier'
    js = os.path.join(d, '{}.json'.format(truck))
    # summarize_data(data, js, term=truck)

    csv_ = os.path.join(d, '{}.csv'.format(truck))
    model(js, csv_)

# =============================================================
