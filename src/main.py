#!/usr/bin/env python3

import os
import sys
import time
import environ

env = environ.Env()

from communicator.deskcommunicator import DeskCommunicator

time.tzset()

PROXY_URL = env.db("PROXY_URL", default="proxy://0.0.0.0:30000")
BROKER_URL = env.db("RABBITMQ_URL")
MONGO_URL = env.db("MONGO_URL")

proxyAddr = PROXY_URL["HOST"]
proxyPort = PROXY_URL["PORT"]
brokerAddr = BROKER_URL["HOST"]
brokerPort = BROKER_URL["PORT"]
logsrvAddr = MONGO_URL["HOST"]
logsrvPort = MONGO_URL["PORT"]
verbose = True

try:
    for index, arg in enumerate(sys.argv):
        match arg:
            case '--addr':
                proxyAddr = sys.argv[index + 1]
            case '--port':
                proxyPort = int(sys.argv[index + 1])
            case '--baddr':
                brokerAddr = sys.argv[index + 1]
            case '--bport':
                brokerPort = sys.argv[index + 1]
            case '--laddr':
                logsrvAddr = sys.argv[index + 1]
            case '--lport':
                logsrvPort = sys.argv[index + 1]
            case '--noverbose':
                verbose = False
except IndexError as ie:
    if verbose:
        print(f'Faltando argumentos para {arg}.', file=sys.stderr)
except TypeError as te:
    if verbose:
        print(f'Argumento de {arg} deve ser um inteiro.', file=sys.stderr)

communicator = DeskCommunicator(
    addr=proxyAddr,
    port=proxyPort,
    rpcAddr=brokerAddr,
    rpcPort=brokerPort,
)

try:
    communicator.start()
except KeyboardInterrupt:
    communicator.close()
    sys.exit(0)
