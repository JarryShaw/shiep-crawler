# -*- coding: utf-8 -*-

import os
import pprint
import re
import urllib
import webbrowser

import bs4
import requests


def crawler(link):
    file = f'{re.sub(r"[:/]+", r"_", link)}.html'
    if not os.path.exists(file) and link.endswith(f'{root}/'):
        webbrowser.open(link)
        input(f'Waiting for {file!r}, press Enter to continue...')
    if os.path.isfile(file):
        with open(file) as file:
            text = file.read()
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
    scheme = rst.scheme.decode() if isinstance(rst.scheme, bytes) else rst.scheme
    netloc = rst.netloc.decode() if isinstance(rst.netloc, bytes) else rst.netloc
    link.add(f'{scheme}://{netloc}/')

pprint.pprint(link)
# re.findall(r'http://[a-zA-Z0-9/.?&;]*\.shiep\.edu\.cn/[a-zA-Z0-9/.?&;]*', text)
