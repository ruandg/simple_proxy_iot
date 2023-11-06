import socket
import threading
import traceback
import sys

from communicator.deviceconnection import DeviceConnection
from communicator.appconnection import AppConnection
from communicator.broker import Broker

class Communicator:

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
        print(f'Executando na porta {self.__port}.')

        while True:
            conn, addr = self.__socket.accept()
            try:
                conn.settimeout(15)
                res = conn.recv(self.__bufferLen)
                res = res.decode()
                sys.stdout.flush()
                if(res == "app"):
                    #app connected
                    #create thread for the app 
                    print("App abriu conexão")
                    data = "ok"
                    conn.send(data.encode("ascii"))
                    sys.stdout.flush()
                    AppConnection(
                        conn, addr, self.__bufferLen, self.__broker).start()
                    continue
                elif len(res) < 8 or len(res) > 13 or (not res.isnumeric()):
                    print(f'Dispositivo ou aplicação {res} falhou em abrir a conexão - ID inválido')
                    data = "fail"
                    conn.send(data.encode("ascii"))
                    sys.stdout.flush()
                    conn.close()
                    continue
                else:
                    print(f'Dispositivo {res} abriu conexão')
                    DeviceConnection(
                        conn, res, addr, self.__bufferLen, self.__broker).start()

            except Exception as ex:
                print(f'Dispositivo {res} falhou em abrir a conexão')
                traceback.print_exception(type(ex), ex, ex.__traceback__)
                continue
           

    def start(self):
        self.__listen()

    def close(self):
        print(f'Encerrando o proxy.')
        self.__socket.close()
