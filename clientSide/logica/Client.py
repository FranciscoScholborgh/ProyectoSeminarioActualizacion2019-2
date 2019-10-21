from __future__ import annotations
from abc import ABCMeta, abstractmethod
from logica.Interfaces import Subject
import socket, Pyro4, time

class ClientNotifier(metaclass=ABCMeta):

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def shutdown(self):
        pass


class TCPClientNotifier(ClientNotifier, Subject):

    def __init__(self, ip_server, puerto):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (ip_server, puerto)
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
            try:
                data = self.sock.recv(pow(2,3))
                command = data.decode('ascii')
                if(command != self.estado_anterior):      
                    if(command == "BREAK IN"):
                        self.estado_anterior = command
                        self.notify()
                    elif(command == "LOCKED"):
                        self.estado_anterior = command
                        self.notify()
                    elif(command == "SHUTDOWN"):
                        self.estado_anterior = command
                        self.notify()
            except:
                self.sock.close()

    def shutdown(self):
        self.activated = False
        self.sock.close()

class UDPClientNotifier(ClientNotifier, Subject):

    def __init__(self, ip_server, puerto):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_address = (ip_server, puerto)
        self.sock.connect(self.server_address)
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
            try:
                message = 'ok'.encode()
                self.sock.sendto(message, self.server_address)
                data, server = self.sock.recvfrom(pow(2,3))
                command = data.decode('ascii')
                if(command != self.estado_anterior):      
                    if(command == "BREAK IN"):
                        self.estado_anterior = command
                        self.notify()
                    elif(command == "LOCKED"):
                        self.estado_anterior = command
                        self.notify()
                    elif(command == "SHUTDOWN"):
                        self.estado_anterior = command
                        self.notify()
            except:
                self.sock.close()

    def shutdown(self):
        self.activated = False
        self.sock.close()

class RMIClientNotifier(ClientNotifier, Subject):

    def __init__(self, ip_server, puerto):
        self.connection = Pyro4.Proxy("PYRO:interface@" + ip_server + ":" + str(puerto))
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
        self.estado_anterior = "LOCKED"
        
        while (self.activated):
            estado = self.connection.getEstado()
            if(estado != self.estado_anterior):
                if(estado == "BREAK IN"):
                    self.estado_anterior = estado
                    self.notify()
                elif(estado  == "LOCKED"):
                    self.estado_anterior = estado 
                    self.notify()
                elif(estado  == "SHUTDOWN"):
                    self.estado_anterior = estado 
                    self.notify()
            time.sleep(0.25)

    def shutdown(self):
        self.activated = False