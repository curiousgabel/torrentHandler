__author__ = 'Mike'

import os
import shutil
from torrenthandler.core import TorrentHandler


class FileMover(TorrentHandler):
    destinationDirectory = ''
    networkDrive = False
    DS = '\\'
    deleteSource = False
    mountDriveLetter = 'P'

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

    def getDestinationDirectory(self):
        return self.destinationDirectory

    def __moveFile(self, sourceFile, destFile):
        result = False
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