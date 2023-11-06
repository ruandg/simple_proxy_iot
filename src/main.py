#!/usr/bin/env python3

import os
import sys
import argparse

from communicator.communicator import Communicator


# Construct the argument parser
ap = argparse.ArgumentParser()

# Add the arguments to the parser
ap.add_argument("-a", "--address", required=True,
   help="IP Address or URL")
ap.add_argument("-p", "--port", required=True,
   help="Port")
args = vars(ap.parse_args())

proxyAddr = args['address']
proxyPort = int(args['port'])

verbose = True

communicator = Communicator(
    addr=proxyAddr,
    port=proxyPort,
)

try:
    communicator.start()
except KeyboardInterrupt:
    communicator.close()
    sys.exit(0)
