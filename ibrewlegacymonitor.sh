#!/bin/bash
echo  iBrew: Rudimentary iKettle monitor
echo  Logging done to ibrewlegacymonitor.log
echo
echo  Usage: ibrewlegacymonitor ip
echo
echo  Press ctrl-c a couple of times to exit
echo  
touch ibrewlegacymonitor.log
while true
do 
    date >> ibrewlegacymonitor.log
    ./ibrewlegacy status $1 | tee -a ibrewlegacymonitor.log
    sleep 1
done