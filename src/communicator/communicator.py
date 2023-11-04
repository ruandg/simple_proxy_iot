import socket
import threading
import json
import traceback
import sys

from communicator.deviceconnection import DeviceConnection
from utils.logging import Logger
from utils.constants import *
from time import sleep
from broker import Broker

class Communicator:

    logger: Logger = Logger.get('proxy')

    def __init__(
        self,
        addr='0.0.0.0',
        port=8080,
        bufferLen=4096,
        backlog=100,
        logAddr='localhost',
        logport=27017
    ):
        self.__addr = addr
        self.__port = port
        self.__bufferLen = bufferLen
        self.__backlog = backlog
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.__broker = Broker()

    def __listen(self):
        self.__socket.bind((self.__addr, self.__port))
        self.__socket.listen(self.__backlog)
        self.__class__.logger.info(f'Executando na porta {self.__port}.')

        while True:
            conn, addr = self.__socket.accept()
            try:
                res = conn.recv(self.__bufferLen)
                res = res.decode("utf-8")
                sys.stdout.flush()
                if(res == "app"):
                    #app connected
                    #create thread for the app 
                    conn.close()
                    continue
                elif len(res) < 8 or len(res) > 13 or (not res.isnumeric()):
                    self.__class__.logger.error(f'Dispositivo ou aplicação {res} falhou em abrir a conexão - ID inválido')
                    data = "fail"
                    conn.send(data)
                    sys.stdout.flush()
                    conn.close()
                    continue
                else:
                    self.__class__.logger.info(f'Dispositivo {res} abriu conexão')
                    DeviceConnection(
                        conn, addr, self.__bufferLen, self.__connected_devices, self.__broker).start()

            except Exception as ex:
                self.__class__.logger.error(f'Dispositivo {res} falhou em abrir a conexão')
                traceback.print_exception(type(ex), ex, ex.__traceback__)
                continue
           

    def start(self):
        self.__listen()

    def close(self):
        self.__class__.logger.info(f'Encerrando o proxy.')

        for desk in DeskConnection.get_authenticated_desks().keys():
            DeskConnection.get_authenticated_desks()[desk].close()

        self.__socket.close()
