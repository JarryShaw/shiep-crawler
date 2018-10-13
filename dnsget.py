# -*- coding: utf-8 -*-

import json
import subprocess
import urllib.parse

with open('domain.json') as file:
    link = json.load(file)

ip = set()
for url in link:
    host = urllib.parse.urlparse(url).netloc
    try:
        stdout = subprocess.check_output(['dnsget', host], stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        print(url, 'failed')
        continue
    address = stdout.split()[-1].decode()
    ip.add(address)
    print(url, address)

with open('ip.json', 'w') as file:
    json.dump(list(ip), file, indent=4)
