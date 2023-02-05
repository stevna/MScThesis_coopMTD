import socket


print("createSocketForIPDisruption was called")
HOST = "192.168.1.10"
PORT = 9999

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

server.listen(5)

while True:
    communication_socket, address = server.accept()
