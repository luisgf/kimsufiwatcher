#!/usr/bin/python3

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
kimsufis = {'KS-6':'150sk60','KS-5':'150sk50','KS-4':'150sk40','KS-3':'150sk30','KS-2 SSD':'150sk22','KS-2':'150sk20','KS-1':'150sk10'}

# Models to watch
watch = ['KS-4'] 

def check_kimsufi(data, model):  
    date = time.strftime('%d/%m/%Y %H:%M:%S')
    if model not in kimsufis:
        print('KimSufi %s model incorrect' % model)
        sys.exit(-1)
    
    soup = BeautifulSoup(data)    
    table = soup.find('table', {'class': 'full homepage-table'})
    tr = table.find('tr', {'data-ref': kimsufis[model]})
    td = tr.find('td', {'class': 'show-on-ref-unavailable elapsed-time-since-last-delivery'})
    
    if 'En cours de réapprovisionnement' in td.text:
        print('%s Kimsufi %s Not Available' % (date, model))
        return True
    else:
        # May be nice to send a mail, TODO
        print('%s Kimsufi %s Available, Go Fast!' % (date, model))
        return False

if __name__ == '__main__':
    rc = True
    while rc:
        r = requests.get('http://www.kimsufi.com/fr/index.xml')

        for model in watch:
            rc = check_kimsufi(r.text, model)
            
        time.sleep(60)
        