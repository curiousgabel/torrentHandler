__author__ = 'Mike'

class Object:

    def __str__(self):
        return self.dump(True)

    def dump(self, returnString = False):
        props = vars(self)
        result = ''

        for item in props.items():
            result = str(item)

        if (not returnString):
            print(result)

        return result

    def setProperty(self, name, value):
        setattr(self, name, value)

    def set(self, name, value):
        self.setProperty(self, name, value)

    def getProperty(self, name):
        result = None

        if name in self.__dict__:
            result = self.__dict__[name]

        return result

    def get(self, name):
        return self.getProperty(self, name)


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
    loggerEnabled = True
    logFile = 'C:\\Users\\Mike\\Documents\\torrentMoverLog.txt'
    details = None

    def __init__(self):
        self.logger = Logger(self.logFile)

    def matches(self):
        self.log('default matcher called')
        return False

    def process(self):
        self.log('default processor called called')
        return False

    def getSourceFileName(self):
        details = self.getDetails()

        return details.fileName

    def getFileName(self):
        details = self.getDetails()

        return details.fileName

    def log(self, message):
        enabled = self.loggerEnabled

        if enabled == True:
            logger = self.logger
            logger.out(message)

    def setDetails(self, details):
        beforeResult = self.beforeSetDetails(details)

        if beforeResult:
            self.details = details
            self.afterSetDetails(details)

    def getDetails(self):
        return self.details

    def beforeSetDetails(self, details):
        return True

    def afterSetDetails(self, details):
        return True