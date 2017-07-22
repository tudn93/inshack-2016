#!/usr/bin/python3
import os
from multiprocessing import Process

BASE_DIR = '/var/www/html/tmp/'

process_list = []
files_to_remove = []

original_phantomjs = ''
with open('phantom.js', 'r') as f:
    original_phantomjs = f.read()

for filename in os.listdir(BASE_DIR):
    lines = original_phantomjs.replace('FILE_NAME_TO_REPLACE', filename)
    temp_phantom = 'temp' + str(len(process_list)) + '.js'
    with open(temp_phantom, 'w') as phantom_parametrised:
        phantom_parametrised.write(lines)

    from subprocess import call
    p = Process(target=call, args=[['phantomjs/bin/phantomjs', '--ignore-ssl-errors=true', '--local-to-remote-url-access=true', '--web-security=false', '--ssl-protocol=any', temp_phantom]])
    process_list.append(p)
    p.start()
    files_to_remove.append(BASE_DIR+filename)
    files_to_remove.append(temp_phantom)

for p in process_list:
	p.join()

for f_to_rm in files_to_remove:
	os.remove(f_to_rm)