echo "" > cpumemoryusage.csv
max=200

i=0
while [ $i -ne $max ]
do
    i=$(($i+1))
    timestamp=$(date)
    cpu=$(echo ""$[100-$(vmstat 1 2|tail -1|awk '{print $15}')]"%")
    echo "$i,$timestamp,%CPU,$cpu,$1" &>> cpumemoryusage.csv
    mem=$(free -h | grep Mem | awk '{print $3}')
    echo "$i,$timestamp,%MEM,$mem,$1" &>> cpumemoryusage.csv
    sleep 2
done
