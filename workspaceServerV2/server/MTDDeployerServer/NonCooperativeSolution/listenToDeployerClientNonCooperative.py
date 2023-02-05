import socket
import sendToDevicesNonCooperative

def main():

    HOST = "192.168.1.10"
    PORT = 5555
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))

    server.listen(5)

    while True:
        communication_socket, address = server.accept()
        print(f"Connected to {address}")
        message = communication_socket.recv(1024).decode("utf-8")
        print(f"Message from clien is: {message}")
        infectedIP = message.split(" ")[2]
        
        print(f"The infected IP is {infectedIP}")
        sendToDevicesNonCooperative.main(infectedIP)
        communication_socket.send(f"Got you message! Thank you New IPs are initialized" .encode("utf-8"))
        communication_socket.close()
        print("Connection ended")
    
if __name__ == "__main__":
    main()