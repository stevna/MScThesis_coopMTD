#!/bin/bash

startTime=0
endTime=0
count=0
overallCount=0

echo "count,startOfInfection,endOfInfection,duration" > /home/MalwareOne/workspace/evaluation/bashliteAnalysisM1.txt

while true; do

  # checks if client process is running
  if pgrep "clientStartScan" > /dev/null
  then
    if [ $startTime -eq 0 ]
    then
      echo "Client running now"
      startTime=$(date +%s%3N)
      startClock=$(date +%T)
    fi
  else
    if [ $startTime -ne 0 ] &&[ $endTime -eq 0 ] 
    then
	echo "start not null, end equals null"
      endTime=$(date +%s%3N)
      endClock=$(date +%T)
    else
      # only prints a message every 25 seconds
      if [[ $((overallCount % 500 )) -eq 0 ]]; then
        startClock=$(date +%T)
        echo "Client not running"
        echo "-1,$startClock" >> /home/MalwareOne/workspace/evaluation/bashliteAnalysisM1.txt
      fi
    fi
  fi

  # if start and endtime is not equal 0, bashlite run and was finished, so log it 
  if [ $startTime -ne 0 ] && [ $endTime -ne 0 ]
  then
    
    elapsedTime=$((endTime-startTime))
    echo "Client ran for $elapsedTime milliseconds"
    echo "$count,$startClock,$endClock,$elapsedTime" >> /home/MalwareOne/workspace/evaluation/bashliteAnalysisM1.txt
    startTime=0
    endTime=0
    ((count=count+1))
  fi
  ((overallCount=overallCount+1))
  sleep 0.05
done
