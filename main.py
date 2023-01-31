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

    result = toyota_search.compile_search()



if __name__ == '__main__':
    main()
    print(time.perf_counter())
# ========================================================
