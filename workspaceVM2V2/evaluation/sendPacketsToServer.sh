#!/bin/bash

host="192.168.1.10"


file="/home/MalwareTwo/workspace/evaluation/pingResults.txt"


echo "time,numberOfPacketsTrans,numberOfPacketsRec,loss,bashliteRun" > $file
bashliteRun=0
increase=false

while true; do
    if pgrep "client" > /dev/null
        then
        if [ "$increase" = true ]
        then
            ((bashliteRun=bashliteRun+1))
            echo "Bashliterun was increased"
            increase=false
        fi
    else
        increase=true
    fi
    
    
    
    result=$(ping -c 1 $host)
    time=$(date +"%T")
    numberOfPacketsTrans=$(echo "$result" | grep -oP "([0-9]+) packets transmitted" | awk '{print $1}')
    numberOfPacketsRec=$(echo "$result" | grep -oP "([0-9]+) received" | awk '{print $1}')
    loss=$(echo "$result" | grep -oP "([0-9]+)% packet loss" | awk '{print $1}')

    echo "$time,$numberOfPacketsTrans,$numberOfPacketsRec,$loss,$bashliteRun" >> $file

    sleep 0.5
done
