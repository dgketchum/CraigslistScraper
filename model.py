import json
import os

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt


def summarize_data(root, out, term='TACOMA'):
    dct = {}
    ct = 0
    _files = [os.path.join(root, x) for x in os.listdir(root)]
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
    err = 0
    x, y, ind, url = [], [], [], []

    for k, v in dct.items():
        try:
            price = float(v['price'])
            if price < 1000:
                continue
            x.append((float(v['odometer']), float(v['year'])))
            y.append(price)
            ind.append(k)
            url.append(v['url'])
        except ValueError:
            err += 1

    y = np.array(y)
    x = np.array(x)
    lr = LinearRegression()
    lr.fit(x, y)
    y_pred = lr.predict(x)
    res = (y - y_pred) / y
    df = pd.DataFrame(data=x.astype(int), columns=['od', 'year'], index=ind)
    df['list_price'] = y.astype(int)
    df['pred_price'] = y_pred.astype(int)
    df['diff'] = res
    df['url'] = url
    df = df.sort_values('diff')
    df.to_csv(csv, float_format='%.2f')


if __name__ == '__main__':
    d = '/home/dgketchum/PycharmProjects/CraigslistScraper/data'
    data = os.path.join(d, '26-Jan-2023')
    js = os.path.join(d, 'tacoma.json')
    # summarize_data(data, js)

    csv_ = os.path.join(d, 'tacoma.csv')
    model(js, csv_)

# =============================================================
