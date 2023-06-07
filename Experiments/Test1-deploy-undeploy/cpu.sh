echo "type,amount,platform" > cpumemoryusage.csv

#numer of attempt
max=10
#number of seconds between one attempt and another
sleep=10

for i in `seq 2 $max`
do
    cpu=$(grep 'cpu ' /proc/stat | awk '{usage=($2+$4)*100/($2+$4+$5)} END {print usage "%"}')
    echo "%CPU,$cpu,$1" &>> cpumemoryusage.csv
    mem=$(free -h | grep Mem | awk '{print $3}')
    echo "%MEM,$mem,$1" &>> cpumemoryusage.csv
    sleep $sleep
done
