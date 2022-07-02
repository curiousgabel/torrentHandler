import json
import re
from urllib.request import urlopen
from urllib.parse import quote

from torrenthandler.core import BaseTestCase

__author__ = 'Mike'


class MovieApi:
    """
    Based off of:
    :link https://epguides-api.readthedocs.org/en/latest/
    """
    baseUrl = 'http://epguides.frecar.no/'
    episodeTitleTemplate = baseUrl + 'show/{showName}/{seasonNumber}/{episodeNumber}/'
    episodeLengthRegex = re.compile('\s*\(\d+\s*min\)$')

    def getEpisodeTitle(self, showName, seasonNumber, episodeNumber):
        """

            :param showName:      str
            :param seasonNumber:  str
            :param episodeNumber: str
            :return : str
            """
        urlData = {
            'showName': showName.replace(' ', ''),
            'seasonNumber': seasonNumber,
            'episodeNumber': episodeNumber
        }
        data = self.send(self.episodeTitleTemplate, urlData)
        result = self.xpathGet(data, 'episode.title', '')
        regex = self.episodeLengthRegex
        result = regex.sub('', result)

        return result

    def makeRequest(self, url):
        data = {}

        try:
            print("calling %s" % url)
            content = urlopen(url).read()
            data = json.loads(content.decode('utf-8'))
        except:
            pass

        return data

    def buildUrl(self, url, data):
        result = url

        for key, value in list(data.items()):
            key = '{' + key + '}'
            result = result.replace(key, quote(str(value)))

        return result

    def send(self, url, data={}):
        url = self.buildUrl(url, data)
        data = self.makeRequest(url)
        # print("Requesting " + url)

        error = 'Empty response' if data == {} else self.xpathGet(data, 'error')
        if error is not None:
            print('IMDB error: ' + error)

        return data

    def xpathGet(self, data, path, default=None):
        item = data
        try:
            for key in path.split('.'):
                item = item.get(key)
        except:
            item = default

        return item


class TestMovieApi(BaseTestCase):
    showName = 'Simpsons'
    seasonNumber = '06'
    episodeNumber = '08'
    episodeTitle = 'Lisa on Ice'
    urlTemplate = 'https://epguides.frecar.no/show/{showName}/{seasonNumber}/{episodeNumber}/'
    completedUrl = 'https://epguides.frecar.no/show/' + showName + '/' + seasonNumber + '/' + episodeNumber + '/'
    responseData = {
        "episode": {
            "release_date": "1994-11-13",
            "show": {
                "imdb_id": "tt0096697",
                "epguide_name": "simpsons",
                "title": "The Simpsons"},
            "number": 8,
            "season": 6,
            "title": "Lisa on Ice"
        }
    }

    def test_getEpisodeTitle(self):
        title = self.testObject.getEpisodeTitle(self.showName, self.seasonNumber, self.episodeNumber)
        self.assertEqual(title, self.episodeTitle)

    def test_makeRequest(self):
        self.assertEqual(self.testObject.makeRequest(self.completedUrl), self.responseData)

    def test_send(self):
        data = {
            'showName': self.showName,
            'seasonNumber': self.seasonNumber,
            'episodeNumber': self.episodeNumber
        }

        self.assertEqual(self.testObject.send(self.urlTemplate, data), self.responseData)

    def test_buildUrl(self):
        data = {
            'showName': self.showName,
            'seasonNumber': self.seasonNumber,
            'episodeNumber': self.episodeNumber
        }

        self.assertEqual(self.testObject.buildUrl(self.urlTemplate, data), self.completedUrl)

    def test_xpathGet(self):
        path = 'episode.show.imdb_id'
        value = 'tt0096697'
        self.assertEqual(self.testObject.xpathGet(self.responseData, path), value)
