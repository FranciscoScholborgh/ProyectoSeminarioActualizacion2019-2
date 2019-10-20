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

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('192.168.1.56', 9001)#67
        self.sock.connect(server_address)
        self.sock.settimeout(None)
        self.activated = False
        self.estado_anterior = "LOCKED"
        self.observers: List[Observer] = []
        print("DO I GET HERE?")
        
    def attach(self, observer: Observer):
        self.observers.append(observer)

    def detach(self, observer: Observer):
        self.observers.remove(observer)

    def notify(self):
        for observer in self.observers:
            observer.update(self.estado_anterior)

    def run(self):
        print("ON THE RUN")
        self.activated = True
        while (self.activated):
            try:
                data = self.sock.recv(pow(2,3))
                command = data.decode('ascii')
                if(command != self.estado_anterior):      
                    if(command == "BREAK IN"):
                        self.estado_anterior = command
                        print("Someony BREAK IN")
                        self.notify()
                    elif(command == "LOCKED"):
                        self.estado_anterior = command
                        print("NOW IT'S LOCKED")
                        self.notify()
                    elif(command == "SHUTDOWN"):
                        self.estado_anterior = command
                        print("SHUTDOWN SERVER")
                        self.notify()
                    else:
                        print("UNKWON COMMAND")
            except:
                self.sock.close()

    def shutdown(self):
        self.activated = False
        self.sock.close()

class UDPClientNotifier(ClientNotifier, Subject):

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_address = ('192.168.1.56', 9001)#67
        self.sock.connect(self.server_address)
        self.sock.settimeout(None)
        self.activated = False
        self.estado_anterior = "LOCKED"
        self.observers: List[Observer] = []
        print("DO I GET HERE?")
        
    def attach(self, observer: Observer):
        self.observers.append(observer)

    def detach(self, observer: Observer):
        self.observers.remove(observer)

    def notify(self):
        for observer in self.observers:
            observer.update(self.estado_anterior)

    def run(self):
        print("ON THE RUN")
        self.activated = True
        while (self.activated):
            try:
                message = 'ok'.encode()
                self.sock.sendto(message, self.server_address)
                data, server = self.sock.recvfrom(pow(2,3))
                print("recibi?")
                command = data.decode('ascii')
                if(command != self.estado_anterior):      
                    if(command == "BREAK IN"):
                        self.estado_anterior = command
                        print("Someony BREAK IN")
                        self.notify()
                    elif(command == "LOCKED"):
                        self.estado_anterior = command
                        print("NOW IT'S LOCKED")
                        self.notify()
                    elif(command == "SHUTDOWN"):
                        self.estado_anterior = command
                        print("SHUTDOWN SERVER")
                        self.notify()
                    else:
                        print("UNKWON COMMAND")
            except:
                self.sock.close()

    def shutdown(self):
        self.activated = False
        self.sock.close()

class RMIClientNotifier(ClientNotifier, Subject):

    def __init__(self):
        self.connection = Pyro4.Proxy("PYRO:interface@192.168.1.56:53546")
        self.estado_anterior = "LOCKED"
        self.observers: List[Observer] = []
        print("Do i get it?")

    def attach(self, observer: Observer):
        self.observers.append(observer)

    def detach(self, observer: Observer):
        self.observers.remove(observer)

    def notify(self):
        for observer in self.observers:
            observer.update(self.estado_anterior)

    def run(self):
        print("ON THE RUN")
        self.activated = True
        self.estado_anterior = "LOCKED"
        
        while (self.activated):
            estado = self.connection.getEstado()
            if(estado != self.estado_anterior):
                if(estado == "BREAK IN"):
                    self.estado_anterior = estado
                    print("Someony BREAK IN")
                    self.notify()
                elif(estado  == "LOCKED"):
                    self.estado_anterior = estado 
                    print("NOW IT'S LOCKED")
                    self.notify()
                elif(estado  == "SHUTDOWN"):
                    self.estado_anterior = estado 
                    print("SHUTDOWN SERVER")
                    self.notify()
                else:
                    print("UNKWON COMMAND")
            time.sleep(0.25)

    def shutdown(self):
        self.activated = False