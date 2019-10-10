import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('192.168.1.67', 9001)
sock.connect(server_address)

try:
    
    # Send data
    message = 'mandame la hora plz :3'.encode()
    sock.sendall(message)
    data = sock.recv(1024)
    print("Data: ", data)

finally:
    sock.close()