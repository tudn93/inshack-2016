import sys, os
from logger import Logger
from encrypt import Encrypt

#
#       CipherFS class
#
class CipherFS:
    def __init__(self, user, password):
        self.user = user
        self.pwd = map(ord, list(password))
        self.storage = ".%s_encrypted" % self.user
        self.logger = Logger(self.map_file("%s_log" % self.user))
        if not os.path.exists(self.storage):
            os.mkdir(self.storage)

    def map_file(self, filename):
        return "%s/enc_%s" % (self.storage, filename)

    def encrypt(self, blist):
        self.logger.debug("computing using (%s)" % (self.pwd))
        e = Encrypt(self.pwd)
        return e.do(blist)

    def write(self, filename):
        self.logger.info("writing file '%s' for user '%s'" % (filename, self.user))
        # fill bytes list
        blist = []
        self.logger.debug("opening file using 'rb' flag")
        with open(filename, 'rb') as cl_file:
            blist = list(bytearray(cl_file.read()))
            cl_file.close()
        # cipher data
        self.logger.debug("ciphering")
        blist = self.encrypt(blist)
        # write output file
        self.logger.debug("writing output file '%s'" % self.map_file(filename))
        with open(self.map_file(filename), 'w') as enc_file:
            enc_file.write(bytearray(blist))
            enc_file.close()
        # delete input file
        self.logger.debug("removing readable file")
        os.remove(filename)

    def read(self, filename):
        # fill bytes list
        blist = []
        self.logger.debug("opening file '%s' using flag 'rb'" % self.map_file(filename))
        with open(self.map_file(filename), 'rb') as enc_file:
            blist = list(bytearray(enc_file.read()))
            enc_file.close()
        # decipher data
        self.logger.debug("deciphering")
        blist = self.encrypt(blist)
        # print file
        self.logger.debug("writing readable file '%s' using 'w' flag" % filename)
        with open(filename, 'w') as cl_file:
            cl_file.write(bytearray(blist))
            cl_file.close()
        # we choose to keep stored file
        self.logger.debug("keeping encrypted file anyway")

    def terminate(self):
        self.logger.flush()
