import re
import os
import shutil

import magic

from torrenthandler.fileMover import Catalog
from torrenthandler.core import BaseTestCase
from torrenthandler.torrent import TorrentDetails

__author__ = 'Mike'


class TvShow:

    showName = ''
    __sourceFileName = ''
    __sourceDirectory = ''
    __showNameReplacement = '[[showName]]'
    __episodeReplacement = '[[episode]]'
    __titleReplacement = '[[title]]'
    __extensionReplacement = '[[extension]]'
    __fileNameTemplate = '[[showName]] [[episode]] - [[title]].[[extension]]'
    episodeSeparator = 'x'

    episodeRegex = re.compile('[0-9]*([0-9]{1,2}?)\D{0,9}([0-9]{1,2})[0-9]*')
    __cleanUpTitleRegexStr = '(\s+-\s+)(\\.)'
    __cleanupSpacesRegexStr = '(\s+)'

    def afterSetDetails(self, details):
        self.__sourceDirectory = details.directory
        self.__sourceFileName = self.getSourceFileName().lower()

    def matches(self):
        result = False
        nameParts = self.showName.split(' ')
        name = self.__sourceFileName
        index = 0

        if len(nameParts) > 0:
            result = True

            for word in nameParts:
                findIndex = name.find(word.lower(), index)
                if findIndex > -1:
                    index = findIndex + len(word)
                else:
                    result = False
                    break

        return result

    def getFileName(self, pretty=True):
        result = self.__sourceFileName

        if result == '':
            files = os.listdir(self.__sourceDirectory)
            for file in files:
                if self.__isVideo(file):
                    result = file
                    break

        if pretty:
            episode = self.getEpisode(result)
            title = self.getTitle()
            extension = self.getExtension(result)
            if extension and (episode is not '' or title is not ''):
                result = self.__fileNameTemplate.replace(self.__showNameReplacement, self.showName)
                result = result.replace(self.__episodeReplacement, episode)
                result = result.replace(self.__titleReplacement, title)
                result = result.replace(self.__extensionReplacement, extension)
                result = self.__cleanupFileName(result)

        return result

    def getSourceFileName(self):
        return self.getFileName(False)

    def getSourceDirectory(self):
        return self.__sourceDirectory

    def getEpisode(self, name):
        result = ''
        regex = self.episodeRegex

        matches = regex.search(name)
        season = matches.group(1)
        episode = matches.group(2)

        if season is not None and episode is not None:
            season = self.__completeNumber(season)
            episode = self.__completeNumber(episode)

            result = season + self.episodeSeparator + episode

        return result

    def getTitle(self):
        result = ''
        # Implement an IMDB API here?

        return result

    def getExtension(self, name):
        result = ''
        name, extension = os.path.splitext(name)

        if extension is not None:
            result = extension.replace('.', '')

        return result

    def __completeNumber(self, num):
        if len(num) < 2:
            num = '0' + num

        return num

    def __cleanupFileName(self, name):
        name = re.sub(self.__cleanupSpacesRegexStr, ' ', name)
        name = re.sub(self.__cleanUpTitleRegexStr, r'\2', name)

        return name

    def __getMediaInfo(self, details):
        result = []

        if details.fileName != '':
            files = [details.directory + '\\' + details.fileName]
        else:
            files = os.listdir(details.directory)


        for file in files:
            fileDetails = magic.from_file(file)

        return result

    def __isVideo(self, filename):
        result = False

        ext = self.getExtension(filename)

        if ext.lower() in ['mp4']:
            result = True

        return result


class TestTvShow(BaseTestCase):
    showName = 'Show Name'
    trackerName = 'tracker.name.com'
    directory = 'C:\\Windows\\Temp'
    fileExtension = 'mp4'
    season = '01'
    episode = '02'
    fileName = 'Show Nameseason' + season + 'episode' + episode + '.' + fileExtension
    prettyFileName = 'Show Name ' + season + 'x' + episode + '.' + fileExtension

    def setupData(self):
        self.testObject.showName = self.showName
        details = [
            self.trackerName,
            self.fileName,
            self.directory
        ]
        self.testDetails = TorrentDetails(details)
        self.setupProperties()
        self.setupFile()
        self.setupDirectory()

    def setupProperties(self):
        self.destinationDirectory = self.directory + '\\tmpfilemovedir'
        self.sourceFile = self.directory + '\\' + self.fileName
        self.destinationFile = self.destinationDirectory + '\\' + self.fileName

    def cleanupData(self):
        self.cleanupFile()
        self.cleanupDirectory()

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

    def test_afterSetDetails(self):
        self.testObject.afterSetDetails(self.testDetails)
        self.assertEqual(self.testObject.getSourceDirectory(), self.directory)
        self.assertEqual(self.testObject.getSourceFileName(), self.fileName.lower())

    def test_matches(self):
        self.testObject.afterSetDetails(self.testDetails)
        self.assertTrue(self.testObject.matches())

        tmp_show_name = self.testObject.showName
        self.testObject.showName = 'noshow'
        self.assertFalse(self.testObject.matches())
        self.testObject.showName = tmp_show_name

    def test_getFileName(self):
        self.testObject.afterSetDetails(self.testDetails)
        self.assertEqual(self.testObject.getFileName(), self.prettyFileName)

    def test_getEpisode(self):
        string = self.season + 'x' + self.episode
        self.assertEqual(self.testObject.getEpisode(self.fileName), string)

    def test_getTitle(self):
        title = ''
        self.assertEqual(self.testObject.getTitle(), title)

    def test_getExtension(self):
        self.assertEqual(self.testObject.getExtension(self.fileName), self.fileExtension)


class TvCatalog(TvShow, Catalog):

    def getDirectoryChain(self):
        showName = self.showName
        fileName = self.getFileName(False)
        episode = self.getEpisode(fileName)
        season, episode = episode.split(self.episodeSeparator)

        return [showName, 'Season ' + season]


class TestTvCatalog(TestTvShow):

    def test_getDirectoryChain(self):
        chain = [self.showName, 'Season ' + self.season]
        self.testObject.afterSetDetails(self.testDetails)
        self.assertEqual(self.testObject.getDirectoryChain(), chain)
