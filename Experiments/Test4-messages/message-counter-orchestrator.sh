#!/bin/bash
echo "Starting counting the packets..."

sudo sysctl -w kernel.yama.ptrace_scope=0
pid=$(ps -ef | grep  "/usr/bin/dockerd" | grep -v grep | awk '{print $2}')
echo " " > strace-orchestrator.txt
timeout 60 strace -f -e trace=network -p $pid -c &>> strace-orchestrator.txt
timeout 60 strace -f -e trace=network -p $pid -c &>> strace-orchestrator.txt
timeout 60 strace -f -e trace=network -p $pid -c &>> strace-orchestrator.txt
timeout 60 strace -f -e trace=network -p $pid -c &>> strace-orchestrator.txt
timeout 60 strace -f -e trace=network -p $pid -c &>> strace-orchestrator.txt
echo "### Finished!! ###"
