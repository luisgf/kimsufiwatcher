#!/usr/bin/env python3

"""
    KimSufi watcher, By Luis González Fernández

    luisgf at luisgf . es, 2015

    Catch a kimsufi server is hard... with this tool i hope
    that your chances to catch one grow a bit.

"""

import requests
import time
import sys
from bs4 import BeautifulSoup

# Kimsufi models
kimsufis = {'KS-5':'160sk5','KS-4A':'160sk4','KS-3B':'160sk31','KS-3A':'160sk3','KS-2A':'160sk2','KS-1':'160sk1'}

# Models to watch
watch = ['KS-3A']

def check_kimsufi(data, model):
    date = time.strftime('%d/%m/%Y %H:%M:%S')
    if model not in kimsufis:
        print('KimSufi %s model incorrect' % model)
        sys.exit(-1)

    soup = BeautifulSoup(data, 'html.parser')
    table = soup.find('table', {'class': 'full homepage-table'})
    tr = table.find('tr', {'data-ref': kimsufis[model]})
    td = tr.find('td', {'class': 'show-on-ref-unavailable elapsed-time-since-last-delivery'})
    qty = td.find('div', {'class':'QTYBox'})

    if qty:
        print('%s Kimsufi %s Not Available' % (date, model))
        return True
    else:
        # May be nice to send a mail, TODO
        print('%s Kimsufi %s Available, Go Fast!' % (date, model))
        return False

if __name__ == '__main__':
    rc = True
    while rc:
        r = requests.get('http://www.kimsufi.com/fr/serveurs.xml')

        for model in watch:
            rc = check_kimsufi(r.text, model)

        time.sleep(60)

