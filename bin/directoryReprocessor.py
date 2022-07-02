"""from torrenthandler.torrent import TorrentDetails
from torrenthandler import customMover
from torrenthandler.torrent import TorrentHandler
import inspect"""
import argparse
import os
from subprocess import call

argParser = argparse.ArgumentParser()
argParser.add_argument("--tracker", help="name of the tracker", required=True)
#argParser.add_argument("--file", help="the name of the item (file or directory) to be processed", required=True)
argParser.add_argument("--directory", help="the directory the downloaded item", required=True)
argParser.add_argument("--category", help="the category of the item", default="")
args = argParser.parse_args()

if not args.directory.endswith("\\"):
    args.directory = args.directory + "\\"
cmdTemplate = "python C:\\Users\\Mike\\Documents\\Projects\\torrenthandler\\bin\\torrentMover.py --tracker=\"%s\" --directory=\"%s\" --category=\"%s\"" % \
              (args.tracker, args.directory, args.category)
cmdTemplate = cmdTemplate+" --file=\"%s\""
print("Opening directory %s" % args.directory)
iters=200
for file in os.listdir(args.directory):
    print("  Processing file %s" % file)
    cmd = cmdTemplate % file
    print("    running %s" % cmd)
    call(["python", "C:\\Users\\Mike\\Documents\\Projects\\torrenthandler\\bin\\torrentMover.py",
          "--tracker", args.tracker,
          "--directory", args.directory,
          "--category", args.category,
          "--file", file])
    #os.system(cmd)
    print("")
    iters = iters-1
    if iters == 0:
        break

"""movers = []
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
"""
