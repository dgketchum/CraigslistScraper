import os
import re
import time
import json
import pandas as pd
from craigslistscraper import Searches


def main():
    """
    Define searches here, a few examples are given below.

    search_name = searches.Searches('your search', 'section')

    default section is 'sss' which is all of craigslist.
    """
    df = pd.read_csv('craigslistscraper/city_data/craigslist_cities_list.csv', header=None)
    cities = list(df[0].values)
    filters = ['&auto_title_status=1']

    toyota_search = Searches('toyota%20tacoma', cities, 'cta', filters, car_data=True)

    # result = toyota_search.compile_search()

    dct = {}
    ct = 0
    _files = [os.path.join('data/26-Jan-2023', x) for x in os.listdir('data/26-Jan-2023')]
    for f in _files:
        with open(f, 'r') as f_:
            js = json.load(f_)
            js = [v for k, v in js.items()][0]
            for city, d in js.items():
                if len(d.keys()) > 0:
                    ct += len(d.keys())
                    for k, v in d.items():

                        dct.update({})
    print(ct, 'cars')
    # dct.update()


if __name__ == '__main__':
    main()
    print(time.perf_counter())
# ========================================================
