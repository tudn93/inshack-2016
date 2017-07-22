#
#    Cette classe permet de generer une nouvelle image contenant des 
#    informations codees sur les 2 bits de poids faible d'une image bitmap
#
class BMPPatcher:
    def __init__(self):
        self.inited = True

    def bmp_info(self, infile):
    	# recuperation du tableau d'octets de l'image BMP
        with open(infile, 'rb') as inf:
            blist = list(bytearray(inf.read()))
            inf.close()
        # generation du tableau d'octets
    	hexlist = map(hex, blist)
    	# affichage des champ du header
        print("--------- BMP HEADER ---------")
        print("BM field      : %s %s" % (hexlist[1], hexlist[0]))
        print("size field    : %s %s %s %s" % (hexlist[5], hexlist[4], hexlist[3], hexlist[2]))
        print("app 1 field   : %s %s" % (hexlist[7], hexlist[6]))
        print("app 2 field   : %s %s" % (hexlist[9], hexlist[8]))
        print("array offset  : %s %s %s %s" % (hexlist[13], hexlist[12], hexlist[11], hexlist[10]))

    def encode(self, infile, outfile, bytes_string):
        # construction du tableau de bits de poids faible
        byte_array = []
        for b in range(len(bytes_string)/2):
            byte_array.append(int('000000'+bytes_string[b*2:b*2+2], 2))
        # recuperation du tableau d'octets de l'image BMP
        with open(infile, 'rb') as inf:
            blist = list(bytearray(inf.read()))
            inf.close()
        # retrieve pixel array start
        index = ""
        for h in range(10,14):
            index = hex(blist[h]).split('x')[1] + index
        index = "0x" + index    
        ind = int(index ,16)
        # check if image is large enough to encapsulate data
        if len(blist) - ind < len(byte_array):
            return False
        # bitwise AND operation applied on pixel array
        for n in range(ind, ind + len(byte_array)):
            print "blist[n] = %d & %d" % (blist[n], byte_array[n-ind])
            blist[n] = blist[n] ^ byte_array[n-ind]
        # write output file
        with open(outfile, 'w') as outf:
            outf.write(bytearray(b for b in blist))
        return True

    def decode(self, infile, length):
        # recuperation du tableau d'octets de l'image BMP
        with open(infile, 'rb') as inf:
            blist = list(bytearray(inf.read()))
            inf.close()
        # retrieve pixel array start
        index = ""
        for h in range(10,14):
            index = hex(blist[h]).split('x')[1] + index
        index = "0x" + index    
        ind = int(index ,16)
        print "reading from offset %s -> %d" % (index, ind)
        # bitwise AND operation applied on pixel array and mask
        bytes_string = ""
        for n in range(ind, min(length, len(blist))):
            print "blist is at %d is %d" % (n, blist[n]) 
            bi = bin(blist[n] & 3).split('b')[1];
            print bi
            if bi == '0':
                bytes_string += '00'
            elif bi == '1':
                bytes_string += '01'
            else:
                bytes_string += '11'
        return bytes_string



