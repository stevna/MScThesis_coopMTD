#!/bin/bash


count=0
while true;do
	echo "restart"
	/home/MalwareOne/workspace/clientStartScanner
	sleep 10
	echo "after first sleep"
	nohup python /home/MalwareOne/workspace/monitoring/sendToDeployerClient.py & > /home/MalwareOne/workspace/runAllNormaly/sendToDeployerClientLogs.txt 2>&1 &
	sleep 110
	echo "after second sleep, should be restarted"
done
