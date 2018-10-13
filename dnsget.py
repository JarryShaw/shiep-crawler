# -*- coding: utf-8 -*-

import json
import subprocess

with open('domain.json') as file:
    link = json.load(file)

ip = set()
for host in link:
    try:
        stdout = subprocess.check_output(['dnsget', host], stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        print(host, 'failed')
        continue
    address = stdout.split()[-1].decode()
    ip.add(address)
    print(host, address)

with open('ip.json', 'w') as file:
    json.dump(list(sorted(ip)), file, indent=4)
