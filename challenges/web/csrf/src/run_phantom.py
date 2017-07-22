#!/usr/bin/python3
import os
from multiprocessing import Process
import requests

BASE_DIR = 'temp_csrf'
URL = 'http://localhost:5000/backdoor-bot-csrf/X1YEGZmNX75vcsHl470CfS9pCvqbDcbajmXS14d2'

resp = requests.get(URL)
session = resp.cookies.get('session')

ids = resp.text.split(';')[:-1]

print(session, ids)

process_list = []
files_to_remove = []

original_phantomjs = ''
with open('phantom.js', 'r') as f:
    original_phantomjs = f.read()

for id_article in ids:
    lines = original_phantomjs.replace('ID_TO_REPLACE', id_article)
    lines = lines.replace('SESSION_TO_REPLACE', session)
    temp_phantom = 'temp' + str(len(process_list)) + '.js'
    with open(temp_phantom, 'w') as phantom_parametrised:
        phantom_parametrised.write(lines)
    
    from subprocess import call
    p = Process(target=call, args=[['phantomjs/bin/phantomjs', '--ignore-ssl-errors=true', '--local-to-remote-url-access=true', '--web-security=false', '--ssl-protocol=any', temp_phantom]])
    process_list.append(p)
    p.start()
    files_to_remove.append(temp_phantom)

for p in process_list:
    p.join()

for f_to_rm in files_to_remove:
    os.remove(f_to_rm)
