#!/usr/bin/python

from morser import Morser
from bmppatcher import BMPPatcher

MESSAGE 	= "good job, you've found the flag : L5B_4ND_M0R53_4R3_FUNNY "
SRC_BMP 	= "imc.bmp"
DEST_BMP 	= "imc_patched.bmp"

# encode string to morse
morser = Morser()
SIZE = morser.bytes_required(MESSAGE)
barray = morser.to_byte_array(MESSAGE)

# create new image patched with morse byte array
bmppatcher = BMPPatcher()
if not bmppatcher.encode(SRC_BMP, DEST_BMP, barray):
	print "image to small for message to be merged"
	exit();

# retrieve morse byte array in image
barray = bmppatcher.decode(DEST_BMP, SIZE*2)

# decode morse byte array using morser
print "decoded string is : %s" % morser.to_string(barray)

