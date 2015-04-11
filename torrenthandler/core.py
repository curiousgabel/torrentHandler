__author__ = 'Mike'

class Object:

    def __str__(self):
        return self.dump(True)

    def dump(self, returnString = False):
        result = vars(self)

        if (not returnString):
            print(result)

        return result

    def setProperty(self, name, value):
        self.__dict__[name] = value


class Logger(Object):
    fileName = ''
    fileHandle = None

    def __init__(self, fileName):
        if fileName is not None and fileName != '':
            self.fileName = fileName
            self.startUp()
        else:
            return False

    def startUp(self):
        self.fileHandle = open(self.fileName, 'a')

    def out(self, text, ending='\n'):
        handle = self.fileHandle
        handle.write(text + ending)


class TorrentHandler(Object):
    stopProcessing = True
    logger = None
    logFile = 'C:\\Users\\Mike\\Documents\\torrentMoverLog.txt'

    def __init__(self):
        self.logger = Logger(self.logFile)

    def matches(self, details):
        self.log('default matcher called')
        return False

    def process(self, details):
        self.log('default processor called called')
        return False

    def getSourceFileName(self, details):
        return details.fileName

    def getFileName(self, details):
        return details.fileName

    def log(self, message):
        logger = self.logger
        logger.out(message)