import socket
from socket import SOL_SOCKET, SO_REUSEADDR
import subprocess
from getpass import getpass
from subprocess import Popen, PIPE, run, check_output, call
import json
import time
import io
import re
from datetime import datetime

print("listenToDeployerServer started")

def writeToLog(logText):
    f = open("/home/MalwareTwo/workspace/evaluation/output.txt", "a")
    text = "{0} PYTHON: {1} \n".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), logText)
    f.write(text)
    print(text)
    f.close()

def getTelnetPort():
    command = '''
    ss -tlnpH | grep inetutils-inetd
    '''
    proc = run(command, stdin=PIPE, shell=True, stdout=PIPE)
    out = proc.stdout.decode("utf-8")
    try:
        x = re.search(r"\:(.*?)\ *0.0.0.0", out)
        telnetPort = x.groups()[0]
        
        delimiter = chr(9)
        command = f"grep telnet /etc/services | sed -n '1p'| cut -f1 -d'/'| cut -f2 -d' ' | cut -f3 -d '{delimiter}'"
        proc = run(command, stdin=PIPE, shell=True, stdout=PIPE)
        portInServiceFile = proc.stdout.decode("utf-8")
        portInServiceFile = portInServiceFile[:-1]  
        if portInServiceFile != telnetPort:
            raise AttributeError
       
    except AttributeError as E:
        #error = "ERROR: It was not possible to get the old telnet port. Error message: ", E 
        writeToLog("ERROR: It was not possible to get the old telnet port. Did you start this Python script with sudo? The error message is: " + str(E))
        telnetPort = False
    return telnetPort

def checkIfTelnetWorks(ownIP, currentPport):
    s = socket.socket()
    s.connect((ownIP, int(currentPport)))
    s.close()
    
globalHOST = socket.gethostbyname(socket.gethostname())
globalPORT = 5555


def listenToDeployer(HOST, PORT ):
    writeToLog("Start listening to deployer Server ")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(5)

    while True:
        communication_socket, address = server.accept()
        writeToLog(f"Connected to {address}")
        count = 0
        maxTry = communication_socket.recv(1024).decode("utf-8")
        communication_socket.send("blublub".encode("utf-8"))
    
        
        while True: 
            commandFromServer = communication_socket.recv(1024).decode("utf-8")
            commandFromServerArray = commandFromServer.split(":")
            movingParameter = commandFromServerArray[0]
            movingParameterValue = commandFromServerArray[1]
            
            if movingParameter == "IP":
                communication_socket.send(f"IP should be changed, movingParameterValue is: {movingParameterValue}".encode("utf-8"))
                writeToLog("Machine infected with malware. Initiating an IP change to the received moving Parameter value: " + movingParameterValue)
                 # need to end the connection because the connection is lost either way due to the IP change
                communication_socket.close()
                writeToLog("The connection to change the IP ended. This is good because this would have happened because of the IP change either way. ")
                
                # need to do this with shell=False because otherwise no useful returncode is returned
                command = ['pkill', '-f', 'client']
                proc = run(command, stdin=PIPE, shell=False, stdout=PIPE)
                print(time.strftime("%H:%M:%S"))
                out = proc.returncode
                print(out)
                if out == 0:
                    writeToLog("Bashlite Client was killed")
                else:
                    writeToLog("There was no Bashlite Client to kill")
                
                command = '''
                sed -i 's/\<{0}\>/{1}/g' /etc/dhcpcd.conf
                ifconfig eth0 down && sudo ifconfig eth0 up
                '''
                
                # this is only needed for the evaluaton because of the
                # unsophisticated Bashlite variant
                if globalHOST == "192.168.1.23":
                    movingParameterValue = "192.168.1.95"
                else:
                    movingParameterValue = "192.168.1.23"
                command = command.format(globalHOST, movingParameterValue)
                proc = run(command, stdin=PIPE, shell=True, stdout=PIPE)
                # we need this sleep because we need to give time to change the IP 
                time.sleep(7)
                currentIP = socket.gethostbyname(socket.gethostname())
                if currentIP != movingParameterValue:
                    writeToLog("The change of the IP address did not work. The current IP address is "+ currentIP + " but it should be: " + movingParameterValue + ".\n\n") 
                else:
                    writeToLog("The change to the IP " + movingParameterValue + " worked. \n\n" )
                return   
                
            elif movingParameter == "port" and count <= int(maxTry):
                count += 1
                # checks if the random port sent by the deployer server is already used
                command = '''
                grep -q "{0}" /etc/services && echo "found" || echo "False" \n
                '''
                command = command.format(movingParameterValue)
                proc = run(command, stdin=PIPE, shell=True, stdout=PIPE)
                out = proc.stdout.decode("utf-8")
                if "found" in out:
                    communication_socket.send("taken".encode("utf-8"))
                    continue
                    
                else:
                    writeToLog("An other Machine was infected with malware. Initiating a port change to the received moving Parameter value: " + movingParameterValue)
                    writeToLog("Port " + movingParameterValue + " is not yet used on this system.")
                    
                    oldTelnetPort = getTelnetPort()
                    if oldTelnetPort == False:
                        communication_socket.send("errorGetTelnetPort".encode("utf-8"))
                        communication_socket.close()
                        writeToLog("Socket closed")
                        return
                        
                    communication_socket.send("not taken".encode("utf-8"))
                    killTelnetProcess(communication_socket)
                    
                    # checks if telnet is currently on port 23
                    try:
                        checkIfTelnetWorks(globalHOST,oldTelnetPort)
                    except ConnectionRefusedError:
                        writeToLog("Telnetport was not accessible, this might be due tue a misconfiguration in the /etc/services file.")
                        communication_socket.send("error".encode("utf-8"))
                        return
                  
                
                  
                    writeToLog("Telnetport was accessible, initiating change")
                    communication_socket.send("getChangeTime".encode("utf-8"))
                    timeToChangeBack = communication_socket.recv(1024).decode("utf-8")
                    changePort(oldTelnetPort, movingParameterValue,communication_socket,timeToChangeBack, globalHOST)
                
                        
                    communication_socket.close()
                    writeToLog("Socket closed")
                    return
            else:
                writeToLog("The port tries exceeded the maximum ports. No port was available on this machine, please provide more ports in the Config file of the Deployer Server.")
                communication_socket.send("exceedMaxTries".encode("utf-8"))
                communication_socket.close()
                writeToLog("Socket closed\n\n")
                return 

            
def killTelnetProcess(communication_socket):
    writeToLog("Trying to kill the telnet process")
    communication_socket.send("not taken".encode("utf-8"))
    
    # kills the telnet service, if the malware has already started to connect 
    command = '''
    sudo pkill telnet && echo "True" || echo "False" \n
    '''
    proc = run(command, stdin=PIPE, shell=True, stdout=PIPE)
    killedTelnet = proc.stdout.decode("utf-8")

    # the killing does work, but it the message here is wrong because of the subprocess
    if killedTelnet == "True":
        communication_socket.send("telnet was killed".encode("utf-8"))
        writeToLog("Telnet process was killed")
    else:
        communication_socket.send("There was something wrong with the telnet kill. There might not be such a process".encode("utf-8"))
        writeToLog("There was something wrong with the telnet process kill. There might not be such a process, so the malware did not yet connect to this device.")
        
def changePort(oldPort,newPort,communication_socket,timeToChangeBack, globalHOST):
    # changes the port of the telnet service
    command = '''
            sed -i 's/\<{0}\>/{1}/g' /etc/services
            sudo systemctl restart inetutils-inetd.service
            '''
    command = command.format(oldPort+"\/tcp", newPort+"\/tcp")
    proc = run(command, stdin=PIPE, shell=True, stdout=PIPE)
    writeToLog("The port change was initiated.")

    command = '''
    grep -q "{0}" /etc/services && echo "found" || echo "False" \n
    '''
    command = command.format(newPort)
    proc = run(command, stdin=PIPE, shell=True, stdout=PIPE)
    serviceCheck = proc.stdout.decode("utf-8")
    if "found" in serviceCheck:
        writeToLog("The changed port was found in services")
    else:
        writeToLog("The new port was not found in services, so something did not work")
        return
        
    
    # checks again if the telnet port is listening 
    try:
        checkIfTelnetWorks(globalHOST, oldPort)
        writeToLog("The new port was found in services, but telnet connection is still possible")
        communication_socket.send("error".encode("utf-8"))
         
    except ConnectionRefusedError: 
        writeToLog("Telnet is not listening anymore, so this worked")
        communication_socket.send("done".encode("utf-8"))
        
        command = '''
        printf "$(date +%F\ %H-%M-%S) SHELL: Sleeping for {0} seconds\n" >> /home/MalwareTwo/workspace/evaluation/output.txt
        sleep {0}
        sed -i 's/\<{1}\>/23\/tcp/g' /etc/services
        sudo systemctl restart inetutils-inetd.service
        sleep 2
        sudo lsof -i:23 && found="true"
        if [ "$found" = "true" ]
        then
            printf "$(date +%F\ %H-%M-%S) SHELL: Went from port {2} back to port 23\n\n\n" >> /home/MalwareTwo/workspace/evaluation/output.txt
        else
            printf "$(date +%F\ %H-%M-%S) SHELL: ERROR: The change back to port 23 failed somehow\n\n\n." >> /home/MalwareTwo/workspace/evaluation/output.txt
        fi       
        '''
        
        command = command.format(timeToChangeBack,newPort+"\/tcp", newPort)
        proc = Popen(command, stdin=PIPE, shell=True, stdout=PIPE)
    return



firstTime = True
while True:
    if not firstTime:
        print("Sleeps for 20 seconds...")
        # this sleep is essential because the change of the IP address might not yet be finished
        time.sleep(20)
    firstTime = False
    globalHOST = socket.gethostbyname(socket.gethostname())
    listenToDeployer(globalHOST, globalPORT)
    print("\n\n")
    


    
#globalHOST = socket.gethostbyname(socket.gethostname())
#listenToDeployer(globalHOST, globalPORT)
