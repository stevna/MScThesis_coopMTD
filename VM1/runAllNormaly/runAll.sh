sudo -v
sudo killall python3
sudo killall python
sudo killall startBashAndSendToDepClient.sh

echo "sleeping for 10 seconds..."
sleep 5
echo "finished sleeping, starting everything"

python -u /home/MalwareOne/workspace/evaluation/CPURamAnalysisMalwareOne.py > CPURamAnalysisMalwareOneLogs.txt 2>&1 & 
sudo python3 -u /home/MalwareOne/workspace/monitoring/listenToDeployerServer.py > listenToDeployerServerLogs.txt 2>&1 & 
sleep 5
pid=$!
echo $pid
pidchild=$(sudo ps -o pid --ppid $pid | sed 1d)
echo $pidchild

/home/MalwareOne/workspace/monitoring/startBashAndSendToDepClient.sh > bashliteClientLogs.txt 2>&1 &

echo "everything should be started, beginning now with CPU and ram usage of listenToDeployerServer"


#echo "time,cpu,ram" > /home/MalwareOne/workspace/evaluation/CPURAMUsage.txt
while true; do
  CPU=$(top -H -p $pidchild -b -n 1 | awk 'NR==8{print $9}')
  RAM=$(top -H -p $pidchild -b -n 1 | awk 'NR==8{print $10}')
  echo -e $(date +%H:%M:%S),$CPU,$RAM >> /home/MalwareOne/workspace/evaluation/CPURAMUsage.txt
#ps -p $pidchild -o %cpu,rss --forest | awk '{ print strftime("%H:%M:%S"), $0 }' | awk '!/%CPU/ && !/RSS/ {print $1 "," $2 "," $3}' >> /home/MalwareOne/workspace/evaluation/CPURAMUsage.txt
  sleep 1
done
