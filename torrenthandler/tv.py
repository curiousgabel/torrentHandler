__author__ = 'Mike'

from abc import ABCMeta, abstractmethod, abstractproperty
import re
import os


class TvShow():

    @abstractproperty
    def showName(self):
        raise NotImplementedError()
    __showNameReplacement = '[[showName]]'
    __episodeReplacement = '[[episode]]'
    __titleReplacement = '[[title]]'
    __extensionReplacement = '[[extension]]'
    __fileNameTemplate = '[[showName]] [[episode]] - [[title]].[[extension]]'
    __episodeSeparator = 'x'

    __episodeRegex = re.compile('[0-9]*([0-9]{1,2})\D{0,9}([0-9]{1,2})[0-9]*')
    __cleanUpTitleRegexStr = '(\s+-\s+)(\\.)'
    __cleanupSpacesRegexStr = '(\s+)'

    def matches(self, details):
        result = False
        nameParts = self.showName.split(' ')
        name = self.getSourceFileName(details)
        index = 0

        if len(nameParts) > 0:
            result = True

            for word in nameParts:
                findIndex = name.find(word, index)
                if findIndex > -1:
                    index = findIndex + len(word)
                else:
                    result = False
                    break

        return result

    def getFileName(self, details):
        result = details.fileName

        episode = self.getEpisode(result)
        title = self.getTitle(result)
        extension = self.getExtension(result)
        if extension and (episode is not '' or title is not ''):
            result = self.__fileNameTemplate.replace(self.__showNameReplacement, self.showName)
            result = result.replace(self.__episodeReplacement, episode)
            result = result.replace(self.__titleReplacement, title)
            result = result.replace(self.__extensionReplacement, extension)
            result = self.__cleanupFileName(result)

        return result

    def getEpisode(self, name):
        result = ''
        regex = self.__episodeRegex

        matches = regex.search(name)
        season = matches.group(1)
        episode = matches.group(2)

        if season is not None and episode is not None:
            season = self.__completeNumber(season)
            episode = self.__completeNumber(episode)

            result = season + self.__episodeSeparator + episode

        return result

    def getTitle(self, name):
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


class NestedTvShow(TvShow):

    def getFileName(self, details, pretty=True):
        result = details.fileName

        if result == '':
            parts = details.directory.split('\\')
            tmpFileName = parts[-1]
            files = os.listdir(details.directory)

            for file in files:
                fileName, extension = os.path.splitext(file)
                if fileName == tmpFileName:
                    result = fileName + extension
                    break

        if pretty:
            details.fileName = result
            result = TvShow.getFileName(self, details)

        return result

    def getSourceFileName(self, details):
        return self.getFileName(details, False)