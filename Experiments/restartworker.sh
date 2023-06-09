pidne=$(ps -ef | grep  "NodeEngine" | grep -v grep | awk '{print $2}')
pidnm=$(ps -ef | grep  "NetManager" | grep -v grep | awk '{print $2}')

echo Restarting Net Manager
sudo kill -9 $pidnm &> /dev/null 2>&1
nohup sudo NetManager -p 6000 &> netmanager.log &
sleep 5
echo Restarting Node Engine
sudo kill -9 $pidne &> /dev/null 2>&1
nohup sudo NodeEngine -n 6000 -p 10100 &> nodeengine.log &