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

    def process(self, details):
        sourceFileName = self.getSourceFileName(details)
        sourceFile = details.directory + self.DS + sourceFileName

        destFileName = self.getFileName(details)
        destFile = self.destinationDirectory + self.DS + destFileName
        result = self.__moveFile(sourceFile, destFile)

        if result and self.deleteSource:
            self.log('deleting ' + sourceFile)
            os.remove(sourceFile)

        return result

    def __moveFile(self, sourceFile, destFile):
        result = False
        self.log('copying ' + sourceFile + ' to ' + destFile)
        print('copying ' + sourceFile + ' to ' + destFile)

        self.__mountDestination()
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