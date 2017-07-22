from Crypto.Cipher import AES
from base64 import b64encode, b64decode
import os, sys

BLOCK = 16
pad = lambda s: s + (BLOCK - len(s) % BLOCK) * chr(BLOCK - len(s) % BLOCK) 
unpad = lambda s : s[0:-ord(s[-1])]

def read_or_make_keys():
	try:
		fkeys = open(".keys", "r")
		key = fkeys.read(32)
		IV = fkeys.read(16)
		fkeys.close()
		return key, IV
	except IOError:
		print "Can't find encryption keys !"
		print "Generating keys ..."
		key = os.urandom(32)
		IV = os.urandom(16)
		fkeys = open(".keys", "w")
		fkeys.write(key + IV)
		fkeys.close()
		print "Keys generated in .keys"
		return key, IV


def encrypt(plaintext, key, IV):
	aes = AES.new(key, AES.MODE_OFB, IV)
	return aes.encrypt(pad(plaintext))

def decrypt(ciphertext, key, IV):
	aes = AES.new(key, AES.MODE_OFB, IV)
	return unpad(aes.decrypt(ciphertext))

if __name__ == '__main__':
	key_AES, IV = read_or_make_keys()
	if len(sys.argv) < 3:
		print "Usage: %s [encrypt|decrypt] filename" % sys.argv[0]
		sys.exit(-1)
	
	mode = sys.argv[1]
	filename = sys.argv[2]
	
	if mode == 'encrypt':
		try:
			infile = open(filename, "r")
			plain = infile.read()
			infile.close()
		except IOError:
			print "Can't find %s" % filename
			sys.exit(-1)
		outfile = open(filename + '.out', "w")
		outfile.write(b64encode(encrypt(plain, key_AES, IV)))
		outfile.close()
	elif mode == 'decrypt':
		try:
			infile = open(filename, "r")
			ciphertext = b64decode(infile.read())
			infile.close()
		except IOError:
			print "Can't find %s" % filename
			sys.exit(-1)
		outfile = open(filename + '.plain', "w")
		outfile.write(decrypt(ciphertext, key_AES, IV))
		outfile.close()
	else: 
		print "Usage: %s [encrypt|decrypt] filename" % sys.argv[0]