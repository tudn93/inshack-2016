#!/usr/bin/env python

import codecs
import re
import random, string
import keyword

def randomword(length):
   return ''.join(random.choice(string.lowercase) for i in range(length))

reversepy = codecs.open('pyreverse.py','w','utf-8')

def encode(code):
	in_str = False
	buffer = []
	if '"' in code:
		for part in code.split('"'):
			if len(part) > 0 and part[-1] == '\\':
				buffer.append(part)
				continue
			if not in_str:
				part = part.encode("rot_13")
			buffer.append(part)
			in_str = not in_str
		return '"'.join(buffer)
	else:
		return code.encode("rot_13")

def obfuNumber(n):
	n = n.group(0)
	# print n
	if '.' in n:
		return n[0] + "(" + str(float(n[1:])*69) + "/3/23)"
	else:
		n0 = n[0]
		neg = False
		if n[1] == '-':
			neg = True
			n = int(n[2:])
		else:
			n = int(n[1:])
	choix = random.randint(0, 3)
	if choix == 0:
		nmod = "(37*0x%x//(~6511%%777))" % (n * 13)
	elif choix == 1:
		nmod = bin(n).replace('L','')
	elif choix == 2:
		nmod = oct(n).replace('L','')
	else:
		k = random.randint(1, 696969)
		nmod = "((%d+3)//%d)" % (n * k - 3, k)
	return n0 + ('-' if neg else '') + nmod

def obfuNumbers(string):
	# fonctionne pour le code du challenge a ne pas reuse
	string = re.sub(r'[ \(=\[,:\+\*]-?[0-9]*\.?[0-9]+', obfuNumber,string)
	return string

def encodeStrings(string):
	all_strings = re.findall(r'".*?"', string)
	for s in all_strings:
		string = string.replace(s, encodeString(s[1:-1]))
	return string

def encodeString(s):
	# print s
	if len(s) == 0:
		return '""'
	s = s.replace('\\n', '\n')
	s = s.replace('\\t', '\t')
	s = s.replace('\\r', '\r')
	s = s.replace('\\"', '"')
	choix = random.randint(0, 3)
	if choix == 0:
		string = s.encode('bz2').encode('hex')
		return '"'+string+'".decode(n.lowercase[7:1:-3]+"x").decode((n.lowercase+"a"*21+n.digits)[1::24])'
	elif choix == 1:
		string = s.encode('base64').replace('\n','')
		return '"'+string+'".decode("4z06uue69sgjanpb"[::-3])'
	elif choix == 2:
		string = '"'
		for i in s:
			hexencoded = hex(ord(i)).replace('0x','')
			string += '\\x' + ('0' + hexencoded if len(hexencoded) == 1 else hexencoded)
		return string.encode('rot13') + '"' # '\x' encode
	else :
		string = []
		for i in s:
			string.append('chr(' + str(ord(i)) + ')')
		return '+'.join(string) # chr()+chr()+...

def renameFunctions(code):
	all_functions = re.findall(r"def\s([\w]+)\s?\(", code)
	new_functions = []
	for function in all_functions:
		new_name = randomword(2)
		while new_name in new_functions or keyword.iskeyword(new_name):
			new_name = randomword(2)
		code = code.replace(function+'(',new_name+'(')
		new_functions.append(new_name)
	return code

def rc4_crypt( data , key ):
	S = range(256)
	j = 0
	out = []
	for i in range(256):
	   j = (j + S[i] + ord( key[i % len(key)] )) % 256
	   S[i] , S[j] = S[j] , S[i]
	i = j = 0
	for char in data:
	   i = ( i + 1 ) % 256
	   j = ( j + S[i] ) % 256
	   S[i] , S[j] = S[j] , S[i]
	   out.append(chr(ord(char) ^ S[(S[i] + S[j]) % 256]))
	return ''.join(out)

def genkey(current_key):
	# '-mofo-' -> 'mastho' -> '-acdh-'
	key = int(current_key.encode('hex'),16)
	new_key = (key ^ 9223371985113708799 + 18446694177406949331) & 9223492302171039855 
	return hex(new_key).replace('0x','').replace('L','').decode("hex")


headers = u'''#!/usr/bin/env python
# -*- coding: rot_13 -*-
'''
# Limitations : 
# chaines doivent etre ecrites entre double quotes
# appel et definitions de fonctions sans espace entre le nom et la parenthese ; exemple : function(vars)
code = u'''
import sys as l
import string as n
cipherkey = "-mofo-"
import time as m
import os as j
cout = l.stdout
slow = 0

def rc4_crypt(data, key):
	S = range(256)
	j = 0
	out = []
	for i in range(256):
	   j = (j + S[i] + ord( key[i % len(key)] )) % 256
	   S[i] , S[j] = S[j] , S[i]
	i = j = 0
	for char in data:
	   i = ( i + 1 ) % 256
	   j = ( j + S[i] ) % 256
	   S[i] , S[j] = S[j] , S[i]
	   out.append(chr(ord(char) ^ S[(S[i] + S[j]) % 256]))
	return "".join(out)

def genKey(key):
	global slow
	if "c" in key:
		slow = 0.001
	key = int(key.encode("hex"),16)
	new_key = (key ^ 9223371985113708799 + 18446694177406949331) & 9223492302171039855 
	return hex(new_key).replace("0x","").replace("L","").decode("hex")

def sleepAndPrint(char):
	m.sleep(0.04 + slow)
	cout.write("\\r"+char)
	cout.flush()

def writeWithStyle(line):
	global slow
	subline = ""
	for _ in line:
		sleepAndPrint(subline+"/")
		sleepAndPrint(subline+"-")
		sleepAndPrint(subline+"\\")
		sleepAndPrint(subline+"|")
		sleepAndPrint(subline+"/")
		subline += _
		slow *= 2
	sleepAndPrint(subline)

home = j.path.expanduser("~")

def decryptAndPrint(data):
	global cipherkey
	writeWithStyle(rc4_crypt(data.decode("hex"),cipherkey))
	print ""
	cipherkey = genKey(cipherkey)

def fakeDeleting(directory):
	compt = 0
	for _ in j.listdir(directory):
		print "# Removing",directory+j.sep+_
		m.sleep(0.4)
		if compt > 8:
			break
		compt += 1
	writeWithStyle("Just kidding :)")

if j.name == "posix" and j.geteuid() != 0:
	writeWithStyle("Run it as root - #INSHACK")
	l.exit(-2)
elif j.name == "nt":
	try:
		j.listdir(j.sep.join([j.environ.get("SystemRoot","C:\\windows"),"temp"]))
	except:
		writeWithStyle("Run it as root - #INSHACK")
		l.exit(-2)

print "--  INSHACK Contest --"
writeWithStyle("I'm r00t oO   ")
print "\\n"
print "\\n"
fakeDeleting(home)

print "\\n"
print "\\n"
try:
	ciphertexts = ["CRYPT_1","CRYPT_2","CRYPT_3","CRYPT_4"]
	decryptAndPrint(ciphertexts[0])
	decryptAndPrint(ciphertexts[1])
	decryptAndPrint(ciphertexts[2])
	decryptAndPrint(ciphertexts[3])
except:
	print "\\nClosing !"
'''
part_1 = 'Welcome to my python reversing challenge !'
part_2 = 'The flag is '
part_3 = '*WAIT* Enabling slow mode...'
part_4 = 'FLAG{it_gonna_be_leg3n_w4it_for_1t_d4ry$!}'

def encode_part(part):
	if not hasattr(encode_part, "counter"):
		encode_part.counter = -1
	encode_part.counter += 1
	if encode_part.counter == 0:
		return rc4_crypt( part , '-mofo-' ).encode('hex')
	if encode_part.counter == 1:
		return rc4_crypt( part , 'mastho' ).encode('hex')
	if encode_part.counter == 2:
		return rc4_crypt( part , '-acdh-' ).encode('hex')
	if encode_part.counter == 3:
		return rc4_crypt( part , 'mastho' ).encode('hex')

code = code.replace('CRYPT_1',encode_part(part_1)).replace('CRYPT_2',encode_part(part_2)).replace('CRYPT_3',encode_part(part_3)).replace('CRYPT_4',encode_part(part_4))

code = code[1:]

variables = ['cipherkey', 'slow', 'cout', 'data', 'new_key','key', 'subline', 'home', 'directory', 'compt', 'ciphertexts']
v_count = 2
for v in variables:
	code = code.replace(v, '_' * v_count)
	v_count += 1

reversepy.write(headers)
code = renameFunctions(code)
code = encodeStrings(code)
code = obfuNumbers(code)
code = encode(code)
code_final = code
reversepy.write(code_final)


reversepy.close()

# print "[!] Code initial [!]"
# print code
# print "\n[!] Code obfu [!]"
# print code_final