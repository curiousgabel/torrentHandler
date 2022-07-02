import os
import shutil

import re

from torrenthandler.torrent import TorrentHandler, TestTorrentHandler

__author__ = 'Mike'


class FileMover(TorrentHandler):
    destinationDirectory = ''
    networkDrive = False
    DS = '\\'
    deleteSource = False
    mountDriveLetter = 'P'
    invalidFileNameCharRegex = re.compile('[\/:*?"<>|]')

    def process(self):
        details = self.getDetails()
        sourceFileName = self.getSourceFileName()
        sourceFile = details.directory
        if sourceFileName != '':
            sourceFile += self.DS + sourceFileName

        destFileName = self.getFileName()
        destDirectory = self.getDestinationDirectory()
        destFile = destDirectory + self.DS + destFileName
        result = self.__moveFile(sourceFile, destFile)

        if result and self.deleteSource:
            self.log('deleting ' + sourceFile)
            os.remove(sourceFile)

        return result

    def cleanFileName(self, filename):
        regex = self.invalidFileNameCharRegex
        path_splitter = '\\'

        if not filename.startswith(path_splitter):
            (drive, path) = filename.split(path_splitter, 1)
            path = regex.sub('', path)
            result = drive + path_splitter + path
        else:
            result = regex.sub('', filename)

        return result

    def getDestinationDirectory(self):
        return self.destinationDirectory

    def __moveFile(self, sourceFile, destFile):
        result = False
        destFile = self.cleanFileName(destFile)
        self.log('copying ' + sourceFile + ' to ' + destFile)

        self.__mountDestination()
        if os.path.isdir(sourceFile):
            shutil.copytree(sourceFile, destFile)
        else:
            shutil.copy2(sourceFile, destFile)
        self.__unmountDestination()

        if os.path.isfile(destFile):
            result = True

        return result

    def __mountDestination(self):
        if self.networkDrive:
            os.system(r"NET USE " + self.mountDriveLetter + ": " + self.destinationDirectory)

    def __unmountDestination(self):
        if self.networkDrive:
            os.system(r"NET USE " + self.mountDriveLetter + ": /DELETE")


class TestFileMover(TestTorrentHandler):
    processReturnValue = True

    def setupData(self):
        TestTorrentHandler.setupData(self)
        self.setupProperties()

        self.testObject.destinationDirectory = self.destinationDirectory
        self.testObject.setDetails(self.testDetails)
        self.setupFile()
        self.setupDirectory()

    def cleanupData(self):
        TestTorrentHandler.cleanupData(self)

        self.cleanupFile()
        self.cleanupDirectory()

    def setupProperties(self):
        self.destinationDirectory = self.directory + '\\tmpfilemovedir'
        self.sourceFile = self.directory + '\\' + self.filename
        self.destinationFile = self.destinationDirectory + '\\' + self.filename

    def setupFile(self):
        if os.path.exists(self.sourceFile) is False:
            open(self.sourceFile, 'a').close()

    def cleanupFile(self):
        if os.path.exists(self.sourceFile):
            os.remove(self.sourceFile)

    def setupDirectory(self):
        if os.path.isdir(self.destinationDirectory) is False:
            os.mkdir(self.destinationDirectory)

    def cleanupDirectory(self):
        if os.path.isdir(self.destinationDirectory):
            shutil.rmtree(self.destinationDirectory)

    def test_getDestinationDirectory(self):
        self.testObject.destinationDirectory = self.destinationDirectory
        self.assertEqual(self.testObject.getDestinationDirectory(), self.destinationDirectory)

    def test_process(self):
        self.testObject.process()
        self.assertTrue(os.path.exists(self.destinationFile))
        self.assertTrue(os.path.exists(self.sourceFile))


class Catalog(FileMover):

    def getDestinationDirectory(self):
        rootDir = self.destinationDirectory
        chain = self.getDirectoryChain()
        chain.insert(0, rootDir)

        result = self.DS.join(chain)
        if not os.path.isdir(result):
            os.makedirs(result)

        return result

    def getDirectoryChain(self):
        return []


class TestCatalog(TestFileMover):
    directoryChain = []

    def test_getDirectoryChain(self):
        self.assertEqual(self.testObject.getDirectoryChain(), self.directoryChain)
