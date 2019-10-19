from abc import ABCMeta, abstractmethod
from logica.Interfaces import Observer
import socket

class Server(metaclass=ABCMeta):

    @abstractmethod
    def run_server(self):
        pass

    @abstractmethod
    def shutdown_server(self):
        pass

class TCPServer(Server, Observer):

    def __init__(self):
        print("TCP RULES")
        self.running = False
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('', 9001)
        self.sock.bind(server_address)
        self.connections: List[connection] = []
        
    def update(self, arg):
        print("Servidor TCP Notificado: ", arg)
        data = arg.encode()
        lost_connections = []
        for cliente in self.connections:
            try:
                cliente.sendall(data)
            except OSError:
                lost_connections.append(cliente)
        for lost in lost_connections:
            self.connections.remove(lost)

    def run_server(self):
        self.running = True
        print("Runing server....")
        while(self.running): 
            self.sock.listen()
            try:
                connection, client_address = self.sock.accept()
                data = "saludos".encode()
                connection.sendall(data)
                self.connections.append(connection)
            except OSError:
                self.update("SHUTDOWN")
                print("RESULTADO: ", self.sock.close())

    def shutdown_server(self):
        self.running = False
        self.sock.close()

class UDPServer(Server, Observer):

    def __init__(self):
        print("UDP RULES")
        self.running = False
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_address = ('', 9001)
        self.sock.bind(server_address)
        self.connections: List[connection] = []
        
    def update(self, arg):
        print("Servidor UDP Notificado: ", arg)
        data = arg.encode()
        lost_connections = []
        for address in self.connections:
            try:
                print("Sending Data: ", data, " From: ", address)
                self.sock.sendto(data, address)
            except OSError:
                lost_connections.append(address)
        for lost in lost_connections:
            self.connections.remove(lost)

    def run_server(self):
        self.running = True
        print("Runing server....")
        while(self.running): 
            #Self.sock.listen()
            try:
                data, address = self.sock.recvfrom(2)
                print("Data: ", data, " From: ", address)
                self.connections.append(address)
            except OSError:
                self.update("SHUTDOWN")
                print("RESULTADO: ", self.sock.close())

    def shutdown_server(self):
        self.running = False
        self.update("SHUTDOWN")
        self.sock.close()

class RMIServer():

    def __init__(self):
        print("TCP RULES")