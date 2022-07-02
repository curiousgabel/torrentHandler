from torrenthandler.torrent import TorrentDetails
from torrenthandler import customMover
from torrenthandler.torrent import TorrentHandler
import inspect
import argparse

argParser = argparse.ArgumentParser()
argParser.add_argument("--tracker", help="name of the tracker", required=True)
argParser.add_argument("--file", help="the name of the item (file or directory) to be processed", required=True)
argParser.add_argument("--directory", help="the directory the downloaded item", required=True)
argParser.add_argument("--category", help="the category of the item", default="")

movers = []
for moverName, mover in inspect.getmembers(customMover, inspect.isclass):
    if inspect.isclass(mover) and issubclass(mover, TorrentHandler):
        movers.append(mover())

movers.sort(key=lambda m: m.priority, reverse=True)

args = vars(argParser.parse_args())
details = TorrentDetails(**args)

for mover in movers:
    mover.setDetails(details)
    if mover.matches():
        print(mover.__class__.__name__ + " matches")
        mover.process()
        if mover.stopProcessing:
            break
