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
        
    def update(self, arg):
        print("Servidor TCP Notificado: ", arg)

    def run_server(self):
        print("Runing server....")
        self.sock.listen()
        connection, client_address = self.sock.accept()
        print("client?")
        while(self.running):      
            #notificacion
            message = fecha.encode()
            connection.sendall(message)
        connection.close()

    def shutdown_server(self):
        self.running = False

class UDPServer():

    def __init__(self):
        print("TCP RULES")

class RMIServer():

    def __init__(self):
        print("TCP RULES")