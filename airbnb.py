#!/usr/bin/env python

import os, sys, csv
import requests
from pprint import pprint
import simplejson as json
import datetime


def get(sort):
    more = True
    offset = 0
    page_size = 50
    results = []

    while more:
        print('fetching {} to {}'.format(offset, offset + page_size))
        try:
            response = requests.get(
                url="https://api.airbnb.com/v2/search_results",
                params={
                    "client_id": "3092nxybyb0otqw18e8nh5nty",
                    "locale": "en-US",
                    "currency": "USD",
                    "_format": "for_search_results",
                    "_limit": str(page_size),
                    "_offset": str(offset),
                    "fetch_facets": "false",
                    "ib": "false",
                    "ib_add_photo_flow": "true",
                    "location": "Long Beach, CA, US",
                    "sort": str(sort),
                },
            )

            if response.status_code == 200:
                results.extend(response.json()['search_results'])
                offset += page_size
            else:
                return results

        except requests.exceptions.RequestException:
            print('HTTP Request failed')

    return results


def save(records, sort):
    os.makedirs('./_data', exist_ok=True)
    path = './_data/{:%Y%m%d_%H%M%S}_{}.json'.format(datetime.datetime.now(), sort)

    with open(path, 'w') as f:
        json.dump(records, f, indent=4, ensure_ascii=False, sort_keys=True)

    return path


pprint('getting records with sort=1')
results = get(1)
saved = save(results, 1)

pprint('getting records with sort=0')
results = get(0)
saved = save(results, 0)

pprint(saved)
pprint('--------------------------------------------------')
print('items: {}'.format(len(results)))