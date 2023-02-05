import json
import socket
import subprocess
from subprocess import Popen, PIPE
import re
import random
import json
import time


def getIPInformation(infectedIP,rootIP,startIPDevices,endIPDevices,serverIP,firstOctettOfRootIP):
    allPossibleIPS = [rootIP + str(i) for i in range(startIPDevices, endIPDevices+1) if i != serverIP]
    eth = subprocess.Popen(["nmap", "-sP", rootIP+str(startIPDevices)+"-"+str(endIPDevices)], stdout=PIPE)
    out, err = eth.communicate()
    alreadyUsedIPS = []
    for line in out.split(b'\n'):
        line = line.lstrip()
        if line.startswith(b'Nmap scan report'):
            alreadyUsedIP = re.search(firstOctettOfRootIP+".*$", str(line, "utf-8")).group(0)
            if alreadyUsedIP != (rootIP+str(serverIP)):
                allPossibleIPS.remove(alreadyUsedIP)
                if alreadyUsedIP != infectedIP:
                    alreadyUsedIPS.append(alreadyUsedIP)
                
    #IPsToChangePort are just all IPs, where the port needs to be changed. So every used IP except the already infected one
    ipObject = {"infectedIP": infectedIP, "allPossibleIPs": allPossibleIPS, "IPsToChangePort": alreadyUsedIPS }
    return ipObject


def executeMTDMechanisms(ipInformation,timeToChangeBack,maxTryOfNewPorts,startOfPossiblePorts,endOfPossiblePorts):
    allPossibleIPS = ipInformation["allPossibleIPs"]
    
    #this is only to prevent the port change for the evaluation
    IPsToChangePort = []
    infectedIP = ipInformation["infectedIP"]
    #usedIPSForThisRun = []
    
    if infectedIP != None:
        try:
            #IP change of the infected
            PORT = 5555
            socketPoint = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socketPoint.connect((ipInformation["infectedIP"], PORT))
            newIP = random.choice(allPossibleIPS)
            allPossibleIPS.remove(newIP)
            # send the max tries in the IP case even if they are not used because the client expects them
            socketPoint.send("-1".encode("utf-8"))
            socketPoint.recv(1024)
            
            sendCommand = "IP:{0}".format(newIP)
            socketPoint.send(sendCommand.encode("utf-8"))
            socketPoint.close()
            
        except OSError as E:
            print("It was not possible to connect to some hosts for the IP change, could it be that they don't listen to the deployer server? The error is: ", E)
    

    for IPToChangePort in IPsToChangePort:
        try:
            print("the IPToChangePort is:", IPToChangePort)
            PORT = 5555
            socketPoint = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socketPoint.connect((IPToChangePort, PORT))
            allPossiblePorts = [str(i) for i in range(int(startOfPossiblePorts),int(endOfPossiblePorts))]
            newPort = random.choice(allPossiblePorts)
            socketPoint.send(str(maxTryOfNewPorts).encode("utf-8"))
            socketPoint.recv(1024)
        
            success = False
            while True:
                while not success:
                    sendCommand = "port:{0}".format(newPort)
                    socketPoint.send(sendCommand.encode("utf-8"))
                    answer = socketPoint.recv(1024)
                    answer = answer.decode("utf-8")
                    if answer == "not taken":
                        success = True
                        
                    elif answer == "errorGetTelnetPort":
                        print("There was an error. This might be due to a problem when searching for the current telnet port in the /etc/services file on the client.")
                        socketPoint.close()
                        return
                        
                    elif answer == "exceedMaxTries":
                        print("There was an error. For the given maximum of ports that should randomly be tried out, no free ports were found on the client. Try to increase the 'maxTryOfNewPorts' or the range of possible ports in the config file.")
                        socketPoint.close()
                        return
                        
                    else:
                        allPossiblePorts.remove(newPort)
                        newPort = random.choice(allPossiblePorts)
                        
                answer = socketPoint.recv(1024).decode()
                print(answer)
                if answer == "done":
                    print("done")
                    socketPoint.close()
                    return
                elif answer == "error":
                    print("There was an error. This might be due to an non-accessible Telnet port.")
                    socketPoint.close()
                    return

                elif answer == "getChangeTime":
                    print("getChangeTime called")
                    socketPoint.send(str(timeToChangeBack).encode("utf-8"))
                    
        except ConnectionRefusedError as E:
                print("It was not possible to connect to some hosts for the port change, could it be that they don't listen to the deployer server?")
    
       
def main(infectedIP):
    with open ("/home/NewMain/workspace/server/MTDDeployerServer/Config.json", "r") as ConfigFile:
        Config = json.load(ConfigFile)

    rootIP = Config["IP"]["rootIP"]
    startIPDevices = Config["IP"]["startIPDevices"]
    endIPDevices = Config["IP"]["endIPDevices"]
    serverIP = Config["IP"]["serverIP"]
    timeToChangeBack = Config["port"]["timeToChangeBack"]
    maxTryOfNewPorts = Config["port"]["maxTryOfNewPorts"]
    firstOctettOfRootIP = rootIP.split(".")[0]
    startOfPossiblePorts = Config["port"]["startOfPossible"]
    endOfPossiblePorts = Config["port"]["endOfPossible"]
    
    ipInformation = getIPInformation(infectedIP,rootIP,startIPDevices,endIPDevices,serverIP,firstOctettOfRootIP)
    executeMTDMechanisms(ipInformation,timeToChangeBack,maxTryOfNewPorts,startOfPossiblePorts,endOfPossiblePorts)

    
    
if __name__ == "__main__":
    main(infectedIP)
    #while True:
    #    main("192.168.1.89")
    #    time.sleep(45)
    #return
#while True:
#    main("192.168.1.11")
#    time.sleep(45)
