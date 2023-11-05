import sys
import socket
import traceback

from threading import Thread, Lock, Semaphore, get_native_id
from queue import Queue, Full
from time import sleep

class AppConnection():

    def __init__(
        self,
        conn: socket.socket,
        addr: tuple,
        bufferLen: int,
        broker = None
    ):        
        self.__id: str = None
        self.__connection: socket.socket = conn
        self.__bufferLen: int = bufferLen
        self.__queue = Queue(10)
        self.__broker = broker


        print(f"Aplicação {addr} conectada.")

 
    def send_data(self, data):
        try:
            self.__queue.put_nowait(data)
        except Exception as ex:
            raise ex

    def __finish(self, active_connection = True):
        print(f"Finalizando tudo para a Aplicação consumindo de {self.__id}.")
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
            self.__connection.send(data.encode("ascii"))
            sys.stdout.flush()
        except Exception as ex:
            raise ex                     

    def __execute(self):
        while True:
            data = self.__queue.get()
            try:
                self.__send(data)
            except Exception:
                print("Erro ao tentar comunicar com a aplicação")
                self.__broker.remove_sub(self)
                self.__finish()
                return

    def start(self):
        res = self.__receive()
        if len(res) < 8 or len(res) > 13 or (not res.isnumeric()):
            print(f'Dispositivo com ID inválido')
            data = "fail"
            try:
                self.__send(data)
            except Exception:
                pass
            self.__finish()
            return
        else:
            self.__id = res
            data = "ok"
            try:
                self.__send(data)
            except:
                pass
            self.__broker.add_subscriber(res, self)
            Thread(target=self.__execute, daemon=False).start()