#!/usr/bin/python

import sys
from py.cipherfs import CipherFS

if len(sys.argv) < 5:
    print "Usage : ./cipher.py (-r|-s) <user> <password> <filename>"
    exit()

option = sys.argv[1]
user = sys.argv[2]
password = sys.argv[3]
filename = sys.argv[4]

c = CipherFS(user, password)

if '-r' in option:
    c.read(filename)
elif '-s' in option:
    c.write(filename)
else:
    print "Unknown option : '%s'" % option
c.terminate()
