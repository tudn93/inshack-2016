from time import gmtime, strftime

#
#       Logger class
#
class Logger:
    def __init__(self, filename):
        self.filename = filename
        self.logs = []

    def flush(self):
        with open(self.filename, 'w') as logfile:
            for log in self.logs:
                logfile.write(log)
            logfile.close()

    def log(self, level, message):
        self.logs.append("(%s)[%s] - %s\n" % (strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime()),level,message))

    def info(self, message):
        self.log("INFO", message)

    def debug(self, message):
        self.log("DEBUG", message)

    def warning(self, message):
        self.log("WARNING", message)

    def error(self, message):
        self.log("ERROR", message)
