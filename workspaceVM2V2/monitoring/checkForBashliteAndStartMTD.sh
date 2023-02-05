#!/bin/bash
shouldRun=true
while true; do
    if pgrep "client" > /dev/null; then
        if [ $(ps -o etimes= -p $(pgrep client)) -gt 10 ]; then
	 if [ $shouldRun = true ]; then
		echo "Python was started"
                python /home/MalwareTwo/workspace/monitoring/sendToDeployerClient.py &
 	        shouldRun=false
	  fi
fi
    else
	shouldRun=true
    fi
    sleep 1
done
