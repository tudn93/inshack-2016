#!/usr/bin/python
#-!- encoding:utf8 -!-

import socket
import time

HOST = '127.0.0.1'    # The remote host
PORT = 50007          # The same port as used by the server

DNS_RECORD = [
'bot1.botnet.botmaster.com',
'bot2.botnet.botmaster.com',
'bot3.botnet.botmaster.com',
'bot4.botnet.botmaster.com',
'bot5.botnet.botmaster.com',
'bot6.botnet.botmaster.com',
'bot7.botnet.botmaster.com',
'bot8.botnet.botmaster.com',
'bot9.botnet.botmaster.com'
]

IP_RECORD = [
'3.1.4.1',
'5.9.2.6',
'5.3.5.8',
'9.7.9.3',
'2.3.8.4',
'6.2.6.4',
'3.3.8.3',
'2.7.9.5',
'0.2.8.8'
]

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

i = -1
j = 0
l = len(IP_RECORD)
while True:
	i+=1
	# mise à jour de i
	if i > l-1:
		i = 0
	# mise à jour de j
	if i % l == l-1:
		j += 1
		if j > l-1:
			j = 0
	# creation du record
	record = "{'dns':'%s','ip':'%s'}" % (DNS_RECORD[ i ], IP_RECORD[ (i+j) % l ])
	s.sendall(record)
	data = s.recv(1024)
	print data
	time.sleep(1)


s.close()

print 'Received', repr(data)