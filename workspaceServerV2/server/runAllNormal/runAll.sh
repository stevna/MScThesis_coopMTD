sudo -v
sudo killall python
sudo killall server
echo "sleeping for 5 seconds..."
sleep 15
echo "finished sleeping, starting everything"

python -u /home/NewMain/workspace/server/MTDDeployerClient/listenToDevices.py > listenToDevicesLogs.txt 2>&1 & 
python -u /home/NewMain/workspace/server/MTDDeployerServer/listenToDeployerClient.py > listenToDeployerClientLogs.txt 2>&1 & 
#python -u /home/NewMain/workspace/server/createSocketForIPDisruption.py > createSocketForIPDisruptionLogs.txt 2>&1 & 
sudo /home/NewMain/workspace/server/server 6667 1 #> serverLogs.txt & #2>&1
echo "everything should be started"
