import json
import os

import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt


def summarize_data(root, out):
    dct = {}
    ct = 0
    _files = [os.path.join(root, x) for x in os.listdir(root)]
    od = 0
    for f in _files:
        with open(f, 'r') as f_:
            js = json.load(f_)
            js = [v for k, v in js.items()][0]
            for city, d in js.items():
                if len(d.keys()) > 0:
                    ct += len(d.keys())
                    for k, v in d.items():
                        basename = os.path.basename(v['url']).split('.')[0]
                        if v['odometer']:
                            od += 1
                            dct[basename] = {'price': v['price'],
                                             'year': v['year'],
                                             'odometer': v['odometer']}

    print('{} complete records'.format(od))
    with open(out, 'w') as _f:
        json.dump(dct, _f, indent=4)


def model(records):
    with open(records, 'r') as _f:
        dct = json.load(_f)
    err = 0
    x, y = [], []
    for k, v in dct.items():
        try:
            x.append((float(v['odometer']), float(v['year'])))
            y.append(float(v['price']))
        except ValueError:
            err += 1
    x = np.array(x)
    lr = LinearRegression()
    lr.fit(x, y)
    pass


if __name__ == '__main__':
    d = '/home/dgketchum/PycharmProjects/CraigslistScraper/data'
    data = os.path.join(d, '26-Jan-2023')
    out = os.path.join(d, 'tacoma.json')
    # summarize_data(data, out)

    model(out)

# =============================================================
