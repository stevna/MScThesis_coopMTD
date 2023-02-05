#!/bin/bash

startTime=0
endTime=0
count=0
overallCount=0

echo "count,startOfInfection,endOfInfection,duration" > /home/MalwareTwo/workspace/evaluation/bashliteAnalysisM2.txt

while true; do

  # checks if client process is running
  if pgrep "client" > /dev/null
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
      if [[ $((overallCount % 500 )) -eq 0 ]]; then
        startClock=$(date +%T)
        echo "Client not running"
        echo "-1,$startClock" >> /home/MalwareTwo/workspace/evaluation/bashliteAnalysisM2.txt
      fi
    fi
  fi

  if [ $startTime -ne 0 ] && [ $endTime -ne 0 ]
  then
    
    elapsedTime=$((endTime-startTime))
    echo "Client ran for $elapsedTime milliseconds"
    echo "$count,$startClock,$endClock,$elapsedTime" >> /home/MalwareTwo/workspace/evaluation/bashliteAnalysisM2.txt
    startTime=0
    endTime=0
    ((count=count+1))
  fi
  ((overallCount=overallCount+1))
  sleep 0.05
done
