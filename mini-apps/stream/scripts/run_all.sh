#/bin/sh

export OMP_NUM_THREADS=12

Usage="./run_all.sh <memory node> <output file>"

if [ $# -ne 2 ]; then
    echo $Usage
    exit 1
fi   

BENCH="../stream"

echo numactl --cpunodebind=0 --membind=$1 $BENCH >> $2
START_TIME=`echo $(($(date +%s%N)/1000000))`
numactl --cpunodebind=0 --membind=$1 $BENCH >> $2
END_TIME=`echo $(($(date +%s%N)/1000000))`
ELAPSED_TIME=$(($END_TIME - $START_TIME))
echo "elapsed time in milliseconds = "$ELAPSED_TIME >> $2
