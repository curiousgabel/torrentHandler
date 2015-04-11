__author__ = 'Mike'

from torrenthandler.core import Object


class TorrentDetails(Object):
    trackerName = ''
    fileName = ''
    directory = ''
    argOrder = ['trackerName',
                'fileName',
                'directory']

    def __init__(self, args):
        torrentDetails = dict(zip(self.argOrder, args))
        for (name, value) in torrentDetails.items():
            self.setProperty(name, value)