# -*- coding: utf-8 -*-

import itertools
import json
import os

import bs4
import requests

with open('ip.json') as file:
    address = json.load(file)

results = list()
for ip in address:
    name = f'tracert/{ip}.json'
    if os.path.isfile(name):
        with open(name) as file:
            traceroute = json.load(file)
        results.append([host['IP'].rjust(15) for host in traceroute])
    else:
        text = requests.post('https://whatismyipaddress.com/traceroute-tool', data=dict(LOOKUPADDRESS=ip)).text
        soup = bs4.BeautifulSoup(text, features='html5lib')

        table = soup.find_all('table')[1]
        context = table.find_all('tr')
        keys = [tag.text for tag in context[0].find_all('td')]

        ip_list = list()
        traceroute = list()
        for body in context[1:]:
            values = [tag.text for tag in body.find_all('td')]
            traceroute.append({key: value for key, value in zip(keys, values)})
            ip_list.append(values[3].rjust(15))

        with open(name, 'w') as file:
            json.dump(traceroute, file, indent=4)
        
        results.append(ip_list)
    print(ip)

print('-'*10)
max_item = max(results, key=lambda ip_list: len(ip_list))
max_length = len(' '.join(max_item))
for ip_list in results:
    print(' '.join(ip_list).rjust(max_length))

with open('route.csv', 'w') as file:
    file.write('Hop,' + ','.join(f'Traceroute_{index+1}' for index, _ in enumerate(results)) + '\n')
    for index, ip_list in enumerate(itertools.zip_longest(*results, fillvalue=' '*15)):
        file.write(f'{index+1},' + ','.join(map(lambda s: s.strip(), ip_list)) + '\n')
os.system('open route.csv')
