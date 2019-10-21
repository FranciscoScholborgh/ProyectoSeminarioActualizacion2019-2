from abc import ABCMeta, abstractmethod
from logica.Interfaces import Observer
import socket, threading, Pyro4

class Server(metaclass=ABCMeta):

    @abstractmethod
    def run_server(self):
        pass

    @abstractmethod
    def shutdown_server(self):
        pass

class TCPServer(Server, Observer):

    def __init__(self):
        self.running = False
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('', 9001)
        self.sock.bind(server_address)
        self.connections: List[connection] = []
        
    def update(self, arg):
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
        while(self.running): 
            self.sock.listen()
            try:
                connection, client_address = self.sock.accept()
                data = "saludos".encode()
                connection.sendall(data)
                self.connections.append(connection)
            except OSError:
                self.update("SHUTDOWN")
                self.sock.close()

    def shutdown_server(self):
        self.running = False
        self.sock.close()

class UDPServer(Server, Observer):

    def __init__(self):
        self.running = False
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_address = ('', 9001)
        self.sock.bind(server_address)
        self.connections: List[connection] = []
        
    def update(self, arg):
        data = arg.encode()
        lost_connections = []
        for address in self.connections:
            try:
                self.sock.sendto(data, address)
            except OSError:
                lost_connections.append(address)
        for lost in lost_connections:
            self.connections.remove(lost)

    def run_server(self):
        self.running = True
        while(self.running): 
            try:
                data, address = self.sock.recvfrom(2)
                self.connections.append(address)
            except OSError:
                self.update("SHUTDOWN")
                self.sock.close()

    def shutdown_server(self):
        self.running = False
        self.update("SHUTDOWN")
        self.sock.close()

@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class ArduinoRMIService(Observer):

    def __init__(self):
        self.estado = "LOCKED"

    def update(self, arg):
        self.estado = arg
    
    def getEstado(self):
        return self.estado

class RMIServer(Server):

    def __init__(self, rmiService : ArduinoRMIService):
        self.service = rmiService

    def run_server (self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        host_name = s.getsockname()[0]
        s.close()
        self.daemon = Pyro4.Daemon(host=host_name, port=9001)
        self.daemon.register(self.service, "interface")
        self.thread = threading.Thread(target=self.daemonLoop)
        self.thread.start()

    def shutdown_server(self):
        self.service.update("SHUTDOWN")
        self.daemon.shutdown()

    def daemonLoop(self):
        self.daemon.requestLoop()