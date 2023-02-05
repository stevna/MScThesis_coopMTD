#!/bin/bash
count=0
while :


do
	if [ $count -eq 0 ]; then
    echo "sleeping for 30 seconds..."
    sleep 20
	else
    echo "sleeping for 60 seconds..."
    sleep 60
	fi
	
	echo "MTD started at: " $(date +%F\ %H-%M-%S)
	python /home/MalwareOne/workspace/monitoring/sendToDeployerClient.py & > /home/MalwareOne/workspace/runAllNormaly/sendToDeployerClientLogs.txt 2>&1 &
	echo "MTD should be started"
	
	count=$((count + 1))
	
done
