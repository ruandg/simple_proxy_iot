import sys
import socket
import traceback

from threading import Thread, Lock, Semaphore, get_native_id
from queue import Queue, Full
from time import sleep

import pika

from utils.logging import Logger

class DeviceConnection():

    logger = Logger.get("device_manager")

    def __init__(
        self,
        conn: socket.socket,
        addr: tuple,
        bufferLen: int,
        connected_devices = None,
    ):        
        self.__stop_threads = False
        self.__id: str = None
        self.__connection: socket.socket = conn
        self.__bufferLen: int = bufferLen
        self.__socket_exception_flag = False
        self.__connected_devices = connected_devices

        Connection.logger.info(f"Dispositivo {addr} conectado.")

    @property
    def _id(self):
        return self.__id

    @property
    def token(self):
        return self.__token
    
   
    def __socket_send_decorator(self, function, data):
        try:
            function(data)
        except Exception as ex:
            self.__socket_exception_flag = True
            raise ex

    def __socket_receive_decorator(self, function):
        data = None
        try:
            data = function()
        except Exception as ex:
            self.__socket_exception_flag = True
            raise ex

        return data
    
    def __finish(self, active_connection = True):
        DeviceConnection.logger.info(f"Finalizando tudo para o Dispositivo {self.__id}.")
        self.__stop_threads = True
        self.__semaphore_ping.release()

        try:
            if(active_connection == False):
                DeviceConnection.logger.info(f"Enviando resposta de erro para o Dispositivo {self.__id}.")
                self.__socket_send_decorator(self.__send, self.__DEFAULT_JSON_RES)
        except:
            pass
     
        try:
            if(active_connection == True and self.__id in self.__connected_desks.keys()):
                self.__connected_devices.pop(self.__id) 
            self.__connection.shutdown(socket.SHUT_RDWR)
            self.__connection.close()
        except:
            pass

        if self.__RPC != None and self.__RPC.is_open():
            try:
                self.__RPC.stop_consuming()
            except:
                return

        return

    def __receive(self) -> dict:
        try:
            data = self.__connection.recv(self.__bufferLen)[:-1]
            sys.stdout.flush()
            data = json.loads(data.decode())
            return data
        except Exception as ex:
            raise ex


    def __send(self, data: dict):
        try:
            data = json.dumps(data)
            self.__connection.send(data.encode())
            sys.stdout.flush()
        except Exception as ex:
            raise ex            

    def __isauthenticated(self):
        return self.__id != None and self.__token != None

    def __login(self):
        try:
            socket_data = self.__socket_receive_decorator(self.__receive)
           
        
        except Exception as ex:
            DeviceConnection.logger.error(f"Falha de comunicação com o dispositivo {self.__id} durante o LOGIN.")
            self.__finish(active_connection = False)
        return

    def __logout(self, _id: str, token: str):
        if _id == self.__id and token == self.__token:
            self.close()



    def execute(self, cmd: dict) -> dict:
        try:
           
        except Exception as ex:
            raise ex
        return ret

    def start(self):
        self.__connection.settimeout(15.0)
        Thread(target=self.__login, daemon=False).start()