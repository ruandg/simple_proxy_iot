#!/usr/bin/env python3

import os
import sys
import time

from communicator.communicator import Communicator

time.tzset()

proxyAddr = "0.0.0.0"
proxyPort = 50000

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
