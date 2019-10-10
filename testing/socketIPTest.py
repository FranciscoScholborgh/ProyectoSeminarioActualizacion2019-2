import socket
import sys
import datetime

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('', 9001)
sock.bind(server_address)
sock.listen()

while True:
    print("listening...")
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
            date = datetime.datetime.now()
            fecha = "fecha: " + str(date.day) + "/" + str(date.month) + "/" + str(date.year) + " - hora: " + str(date.hour)  + ":" + str(date.minute) + ":" + str(date.second)
            message = fecha.encode()
            connection.sendall(message)
    except(ConnectionAbortedError):
        pass
    finally:
        # Clean up the connection
        connection.close()
        print("close")
        print("continue xD")
