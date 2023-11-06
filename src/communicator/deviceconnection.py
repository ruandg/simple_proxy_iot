import sys
import socket
import traceback

from threading import Thread
from communicator.broker import Broker

class DeviceConnection():

    def __init__(
        self,
        conn: socket.socket,
        id: None,
        addr: tuple,
        bufferLen: int,
        broker = None
    ):        
        self.__stop_threads = False
        self.__id: str = id
        self.__connection: socket.socket = conn
        self.__bufferLen: int = bufferLen
        self.__socket_exception_flag = False
        self.__broker = broker

        print(f"Dispositivo {addr} conectado.")


    @property
    def _id(self):
        return self.__id
    
    def __finish(self, active_connection = True):
        print(f"Finalizando tudo para o Dispositivo {self.__id}.")
        self.__stop_threads = True
        try:
            self.__connection.shutdown(socket.SHUT_RDWR)
            self.__connection.close()
        except:
            pass
        return

    def __receive(self) -> str:
        try:
            data = self.__connection.recv(self.__bufferLen)
            sys.stdout.flush()
            data = data.decode("utf-8")
            return data
        except Exception as ex:
            raise ex

    def __send(self, data: str):
        try:
            print(f"Sending...{data}")
            self.__connection.send(data.encode("ascii"))
            sys.stdout.flush()
        except Exception as ex:
            raise ex            

    def __execute(self):
        while True:
            try:
                socket_data = self.__receive()
                if(socket_data == "alive"):
                    print(f"Dipositivo {self.__id} está vivo.")
                elif(socket_data.isnumeric()):
                    print(f"{self.__id} publicando {socket_data} no broker.")
                    self.__broker.publish(self.__id,socket_data)
                else:
                    print(f"Dispositivo {self.__id} fechou conexão.")
                    self.__broker.remove_pub(self.__id)
                    self.__finish()
                    return
            except Exception as ex:
                print(f"Erro comunicando com o Dispositivo {self.__id}.")
                traceback.print_exception(type(ex), ex, ex.__traceback__)
                self.__broker.remove_pub(self.__id)
                self.__finish()
                return


    def start(self):
        ret = self.__broker.add_publisher(self.__id)
        if(not ret):
            print(f"Já existe dispositivo com ID {self.__id} conectado.")
            data = "fail"
            try:
                self.__send(data)
            except Exception as ex:
                print(f"Erro enviando fail ao Dispositivo {self.__id}.")
                traceback.print_exception(type(ex), ex, ex.__traceback__)
            self.__finish()
            return
        else:
            data = "ok"
            try:
                self.__send(data)
            except Exception as ex:
                print(f"Erro enviando ok ao Dispositivo {self.__id}.")
                traceback.print_exception(type(ex), ex, ex.__traceback__)
                self.__broker.remove_pub(self.__id)
                self.__finish()
            Thread(target=self.__execute, daemon=False).start()