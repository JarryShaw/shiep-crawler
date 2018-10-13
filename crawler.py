# -*- coding: utf-8 -*-

import json
import os
import pprint
import urllib.parse
import webbrowser

import bs4
import requests


def crawler(link):
    file = f'{urllib.parse.urlparse(link).netloc}.html'
    path = f'html/{file}'
    if not os.path.exists(path) and link.endswith(f'{root}/'):
        webbrowser.open(link)
        input(f'Waiting for {file!r}, press Enter to continue...')
    if os.path.isfile(path):
        with open(path) as html:
            text = html.read()
    else:
        try:
            text = requests.get(link).text
        except requests.exceptions.ConnectionError:
            return set()
    soup = bs4.BeautifulSoup(text, features='html5lib').find_all('a')

    href = list()
    for atag in soup:
        url = atag.get('href', '')
        rst = urllib.parse.urlparse(url)
        scheme = rst.scheme.decode() if isinstance(rst.scheme, bytes) else rst.scheme
        netloc = rst.netloc.decode() if isinstance(rst.netloc, bytes) else rst.netloc
        if root in netloc:
            href.append(url)
        elif 'http' in scheme:
            continue
        else:
            href.append(f'http://www.{root}/{url.lstrip("/")}')
    return set(href)


root = 'shiep.edu.cn'
link = f'http://www.{root}/'
href = crawler(link)
todo = list(href)
done = [link]

print(link)
# pprint.pprint(href)
# pprint.pprint(done)
# pprint.pprint(todo)
print('-'*10)

for link in todo:
    if link in done:
        todo.remove(link)
        continue
    href.union(crawler(link))
    todo.remove(link)
    done.append(link)

    print(link)
    # pprint.pprint(href)
    # pprint.pprint(done)
    # pprint.pprint(todo)
    print('-'*10)

pprint.pprint(href)
print('-'*10)

link = set()
for url in href:
    rst = urllib.parse.urlparse(url)
    netloc = rst.netloc.decode() if isinstance(rst.netloc, bytes) else rst.netloc
    link.add(netloc)

pprint.pprint(link)
with open('domain.json', 'w') as file:
    json.dump(list(sorted(link)), file, indent=4)
# re.findall(r'http://[a-zA-Z0-9/.?&;]*\.shiep\.edu\.cn/[a-zA-Z0-9/.?&;]*', text)
