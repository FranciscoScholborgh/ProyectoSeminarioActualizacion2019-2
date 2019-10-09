import socket
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


server_address = ("192.168.1.67", 9001)
print(socket.gethostname())
sock.bind(server_address)
sock.listen()

while True:
    # Wait for a connection
    connection, client_address = sock.accept()
    print("alguien se conecto: ", client_address)
    try:
        # Receive the data in small chunks and retransmit it
        while True:
            data = connection.recv(1024)
            if not data:
                print('no more data from', client_address)
                connection.close()
                break
            print(data)   
            connection.sendall(data)
    except(ConnectionAbortedError):
        pass
    finally:
        # Clean up the connection
        connection.close()
        print("close")
        print("continue xD")
