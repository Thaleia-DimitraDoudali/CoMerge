#/bin/sh

Usage="./run_all.sh <memory node> <output file>"

if [ $# -ne 2 ]; then
    echo $Usage
    exit 1
fi   

BENCH="../my_clomp 12 1 64000 640 32 1 100"

echo numactl --cpunodebind=0 --membind=$1 $BENCH >> $2
START_TIME=`echo $(($(date +%s%N)/1000000))`
numactl --cpunodebind=0 --membind=$1 $BENCH >> $2
END_TIME=`echo $(($(date +%s%N)/1000000))`
ELAPSED_TIME=$(($END_TIME - $START_TIME))
echo "elapsed time in milliseconds = "$ELAPSED_TIME >> $2
