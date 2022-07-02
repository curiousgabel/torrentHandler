from os import remove

from torrenthandler.core import Object, Logger, BaseTestCase

__author__ = 'Mike'


class TorrentDetails(Object):
    trackerName = None
    fileName = None
    directory = None
    category = None

    def __init__(self, file='', directory='', tracker='', category=''):
        self.fileName = file
        self.directory = directory
        self.trackerName = tracker
        self.category = category

    def __str__(self):
        return "trackerName: %s\nfileName: %s\ndirectory: %s\ncategory: %s""" % (self.trackerName, self.fileName, self.directory, self.category)


class TestTorrentDetails(BaseTestCase):
    trackerName = 'tracker.name.com'
    filename = 'file_name.tmp'
    directory = '/dir/etc/ory'
    category = 'movies'
    objectParams = {
        'args': [
            trackerName,
            filename,
            directory,
            category
        ]
    }

    def test__init__(self):
        tracker_name = self.testObject.getProperty('trackerName')
        filename = self.testObject.getProperty('fileName')
        directory = self.testObject.getProperty('directory')
        category = self.testObject.getProperty('category')

        self.assertEqual(self.trackerName, tracker_name)
        self.assertEqual(self.filename, filename)
        self.assertEqual(self.directory, directory)
        self.assertEqual(self.category, category)


class TorrentHandler(Object):
    stopProcessing = True
    logger = None
    loggerEnabled = True
    logFile = 'C:\\Users\\Mike\\Documents\\torrentMoverLog.txt'
    details = None
    priority = 10

    def __init__(self, logfile=None):
        if logfile is None:
            logfile = self.logFile
        else:
            self.logFile = logfile

        self.logger = Logger(logfile)

    def matches(self):
        self.log('default matcher called')
        return False

    def process(self):
        self.log('default processor called')
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
            print(message)

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


class TestTorrentHandler(BaseTestCase):
    matchesReturnValue = False
    processReturnValue = False
    trackerName = 'tracker.name.com'
    directory = 'C:\\Windows\\Temp'
    filename = 'file_name.tmp'
    logfile = directory + '\\tmplogfile'
    testLogMessage = 'this is a logging message'

    objectParams = {
        'logfile': logfile
    }

    def setupData(self):
        details = [
            self.trackerName,
            self.filename,
            self.directory
        ]
        self.testDetails = TorrentDetails(details)

    def cleanupData(self):
        del self.testDetails
        remove(self.logfile)

    def test_matches(self):
        self.assertEqual(self.testObject.matches(), self.matchesReturnValue)

    def test_process(self):
        self.assertEqual(self.testObject.process(), self.processReturnValue)

    def test_getFileName(self):
        self.testObject.setDetails(self.testDetails)
        self.assertEqual(self.testObject.getFileName(), self.filename)

    def test_getSourceFileName(self):
        self.testObject.setDetails(self.testDetails)
        self.assertEqual(self.testObject.getSourceFileName(), self.filename)

    def test_log(self):
        self.testObject.log(self.testLogMessage)
        self.testObject.logger.close()

        handle = open(self.logfile, 'r')
        data = handle.read()
        handle.close()

        self.testObject.logger.open()

        str_contains = self.testLogMessage in data

        self.assertTrue(str_contains)

    def test_setDetails(self):
        self.testObject.setDetails(self.testDetails)

        self.assertEqual(self.testObject.details, self.testDetails)

    def test_getDetails(self):
        self.testObject.setDetails(self.testDetails)

        self.assertEqual(self.testObject.getDetails(), self.testDetails)

    def test_beforeSetDetailsReturnsTrue(self):
        self.assertTrue(self.testObject.beforeSetDetails(self.testDetails))

    def test_afterSetDetails(self):
        self.assertTrue(self.testObject.afterSetDetails(self.testDetails))