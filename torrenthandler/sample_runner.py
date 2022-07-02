import torrenthandler.fileMover
import torrenthandler.tv
from torrenthandler.tv import TvShowDecorator
import os
import re

# The generic mover for by NAS (named thewarehouse)
class WarehouseMover(torrenthandler.fileMover.FileMover):
    destinationDirectory = '\\\\thewarehouse\\media\\Videos'


# Sample of a simple recurring TV show
class RickAndMortyMover(torrenthandler.tv.TvShow, WarehouseMover):
    showName = 'Rick and Morty'

# Sample of a recurring TV show that requires a special regex to pull the season
# and episode numbers out of the file name
class Archer(torrenthandler.tv.TvShow, WarehouseMover):
    showName = 'Archer'
    episodeRegex = re.compile('2009\D+([0-9]{1,2})\D{0,9}([0-9]{1,2})[0-9]*')


# Sample of a recurring show where the show name on the torrent is different than the show name
# in the TV show API
class LastWeekTonightMover(torrenthandler.tv.TvShow, WarehouseMover):
    showName = 'Last Week Tonight'
    apiShowName = 'LastWeekTonightwithJohnOliver'

    def afterSetDetails(self, details):
        torrenthandler.tv.TvShow.afterSetDetails(self, details)


# My "movie mover"; works based on category assigned to the torrent in the client
# I currently use Vuze, but want a lighter weight client that supports category assignment,
# RSS feeds, and post-download commands
class MovieMover(WarehouseMover):
    # Moves the file to a specific directory instead of determining it based on show/season
    destinationDirectory = '\\\\thewarehouse\\media\\Videos\\Movies'

    def matches(self):
        result = False
        details = self.getDetails()

        if details.category == 'movies':
            result = True

        return result

    """Stole all the below from TvShow; should make that more generic"""
    def __isVideo(self, filename):
        result = False

        ext = self.getExtension(filename)

        if ext.lower() in ['mp4', 'mkv', 'avi']:
            result = True

        return result

    """ Needs a test case"""
    def getFileName(self):
        result = self.getSourceFileName().lower()

        if result == '':
            files = os.listdir(self.details.directory)
            for file in files:
                if self.__isVideo(file):
                    result = file
                    break

        return result

    def getExtension(self, name):
        result = ''
        name, extension = os.path.splitext(name)

        if extension is not None:
            result = extension.replace('.', '')

        return result
