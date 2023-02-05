import socket
import time
import telnetlib

serverIP = '192.168.1.10'
serverPort = 23
serverTries = 0
serverFails = 0
serverFailTime = 0
serverStartTime = time.time()


with open("/home/MalwareTwo/workspace/evaluation/telnetToServer.txt", "w") as file:
    file.write("time,")
    file.write("telnetToServerPossible\n")
    

def TelnetDisruptionToServer(file, IP, port, tries, fails, failTime,startTime):
    file.write(time.strftime("%H:%M:%S")+",")
    try:
        print("started")
        telnetConnection = telnetlib.Telnet(IP,port,timeout=1)
        print("before close")
        telnetConnection.close()
        print("the connection was established")
        file.write("True\n")
        #file.write(str(failTime))
    except OSError:
        fails += 1
        failTime += time.time() - startTime
        startTime = time.time()
        file.write("False\n")
        #file.write(str(failTime))
        print("the connection failed")
    tries += 1

while True:
    with open("/home/MalwareTwo/workspace/evaluation/telnetToServer.txt", "a") as file:
        TelnetDisruptionToServer(file, serverIP, serverPort, serverTries, serverFails, serverFailTime,serverStartTime)
    time.sleep(0.5)
