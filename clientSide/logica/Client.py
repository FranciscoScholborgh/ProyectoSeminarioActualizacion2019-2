from __future__ import annotations
from abc import ABCMeta, abstractmethod
from logica.Interfaces import Subject
import socket

class ClientNotifier(metaclass=ABCMeta):

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def shutdown(self):
        pass


class TCPClientNotifier(ClientNotifier, Subject):

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('192.168.1.67', 9001)
        self.sock.connect(server_address)
        self.sock.settimeout(None)
        self.activated = False
        self.estado_anterior = "LOCKED"
        self.observers: List[Observer] = []
        

    def attach(self, observer: Observer):
        self.observers.append(observer)

    def detach(self, observer: Observer):
        self.observers.remove(observer)

    def notify(self):
        for observer in self.observers:
            observer.update(self.estado_anterior)

    def run(self):
        self.activated = True
        while (self.activated):
            data = sock.recv(pow(2,3))
            command = data.decode('ascii')
            if(command != self.estado_anterior):      
                if(command == "BREAK IN"):
                    self.estado_anterior = command
                    print("Someony BREAK IN")
                elif(command == "LOCKED"):
                    self.estado_anterior = command
                    print("NOW IT'S LOCKED")
                else:
                    print("UNKWON COMMAND")


    def shutdown(self):
        self.activated = False
        self.sock.close()


