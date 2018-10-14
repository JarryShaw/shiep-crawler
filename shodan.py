# -*- coding: utf-8 -*-

import copy
import ipaddress
import json
import os
import time

import requests

API_KEY = '6JJ0qCCNHzv6iLsPvUPQNst0Dpbh87io'

with open('info/failed.json') as file:
    failed = json.load(file)

http = dict()
for ip in ipaddress.ip_network('210.35.88.0/24'):
    name = f'info/{ip}.json'
    if os.path.isfile(name):
        with open(name) as file:
            context = json.load(file)
    elif str(ip) in failed:
        print(ip, 'pass')
        continue
    else:
        request = requests.get(f'https://api.shodan.io/shodan/host/{ip}?key={API_KEY}')
        if not request.ok:
            print(ip, request.status_code)
            failed.append(str(ip))
            continue
        context = request.json()
        with open(name, 'w') as file:
            json.dump(context, file, indent=4)
        time.sleep(1)

    port = list()
    for data in context['data']:
        if 'http' in data:
            port.append(str(data['port']))
    http[ip] = copy.copy(port)
    print(ip, port)

with open('http.csv', 'w') as file:
    file.write('IP,Ports\n')
    for ip, port in http.items():
        if port:
            file.write(f'{ip},{",".join(sorted(port, key=int))}\n')

with open('info/failed.json', 'w') as file:
    json.dump(failed, file, indent=4)
