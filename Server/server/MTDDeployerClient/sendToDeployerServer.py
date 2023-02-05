import socket

def send(address):
    print("The virus was found on IP address: ", address)
    HOST = "192.168.1.10"
    PORT = 5555
    socketPoint = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socketPoint.connect((HOST, PORT))
    print("send called")
    message = f"Virus found {address}"
    print(f"this is the message: {message}")
    socketPoint.send(message.encode("utf-8"))
    print(socketPoint.recv(1024))
    socketPoint.close()
    
    

if __name__ == "__main__":
    send(address)
    

    


#send()