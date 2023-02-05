#!/bin/bash

while :
do
	if pgrep "clientStartScan" > /dev/null
	then
		echo "Time over, but bashlite is still running"
		sleep 5
	else
	echo "should be restarted"
	/home/MalwareOne/workspace/clientStartScanner &
	rand_num=$(shuf -i 60-120 -n 1)
	echo "Bash started at: " $(date +%F\ %H-%M-%S)
	echo $rand_num
	sleep $rand_num
	fi
done

