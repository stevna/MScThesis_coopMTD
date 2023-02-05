sudo -v
sudo killall python
sudo killall server
sudo fuser -k 6667/tcp
echo "sleeping for 15 seconds..."
sleep 15
echo "finished sleeping, starting everything"

python -u /home/NewMain/workspace/server/MTDDeployerClient/listenToDevices.py > listenToDevicesLogs.txt 2>&1 & 
python -u /home/NewMain/workspace/server/MTDDeployerServer/NonCooperativeSolution/listenToDeployerClientNonCooperative.py > listenToDeployerClientNonCooperativeLogs.txt 2>&1 & 
#python -u /home/NewMain/workspace/server/createSocketForIPDisruption.py > createSocketForIPDisruptionLogs.txt 2>&1 & 
sudo /home/NewMain/workspace/server/server 6667 1 # > serverLogs.txt 2>&1
echo "everything should be started"
