#!/bin/bash
echo "time,telnetToLocalPossible" > /home/MalwareTwo/workspace/evaluation/telnetToLocal.txt
while true
do
  timestamp=
  nc -z -w 1 192.168.1.23 23
  if [ $? -eq 0 ]; then
    echo "$(date +%H:%M:%S),True" >> /home/MalwareTwo/workspace/evaluation/telnetToLocal.txt
  else
    nc -z -w 1 192.168.1.95 23
    if [ $? -eq 0 ]; then
      echo "$(date +%H:%M:%S),True" >> /home/MalwareTwo/workspace/evaluation/telnetToLocal.txt
    else
      echo "$(date +%H:%M:%S),False" >> /home/MalwareTwo/workspace/evaluation/telnetToLocal.txt
    fi
  fi
  sleep 0.5
done
