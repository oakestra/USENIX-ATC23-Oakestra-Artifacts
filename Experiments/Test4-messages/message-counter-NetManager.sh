#!/bin/bash
echo "Starting counting the packets..."

sudo sysctl -w kernel.yama.ptrace_scope=0
pid=( $(ps -ef | grep  "NetManager" | grep -v grep | awk '{print $2}') )
echo " " > strace-net-manager.txt
timeout 60 strace -f -e trace=network -p ${pid[1]} -c &>> strace-net-manager.txt
timeout 60 strace -f -e trace=network -p ${pid[1]} -c &>> strace-net-manager.txt
timeout 60 strace -f -e trace=network -p ${pid[1]} -c &>> strace-net-manager.txt
timeout 60 strace -f -e trace=network -p ${pid[1]} -c &>> strace-net-manager.txt
timeout 60 strace -f -e trace=network -p ${pid[1]} -c &>> strace-net-manager.txt
echo "### Finished!! ###"
