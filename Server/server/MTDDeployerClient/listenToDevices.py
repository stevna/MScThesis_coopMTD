import socket
import json
import sendToDeployerServer
from _thread import *

# print(socket.gethostbyname(socket.gethostname()))
# print(socket.gethostname())


#HOST = "10.10.10.2"
HOST = "192.168.1.10"
PORT = 6669
threadCount = 0


def acceptConnections(server):
    communication_socket, address = server.accept()
    start_new_thread(clientHandler, (communication_socket, address))

def clientHandler(communication_socket, address):
    count = 0
    IPAddress = address[0]

     
    print(f"Connected to {IPAddress}")
    message = communication_socket.recv(1024).decode()
    if message == "virus":
        sendToDeployerServer.send(IPAddress)
        count += 1
        communication_socket.send("Got virus message".encode("utf-8"))

    communication_socket.close()
    print("Connection ended")


def startServer():
    print("listenToDevices was called")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(f"server: {server}")
    server.bind((HOST, PORT))
    server.listen(5)

    while True:
        acceptConnections(server)


if __name__ == "__main__":
    startServer()

