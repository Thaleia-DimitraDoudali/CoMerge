#/bin/sh

BENCH="/home/thaleia/comerge/mini-apps/XSBench/src/XSBench -s large -t 4 -g 2000 -l 50000000"

START_TIME=`echo $(($(date +%s%N)/1000000))`
numactl --cpunodebind=0 --membind=0 $BENCH >> $1
END_TIME=`echo $(($(date +%s%N)/1000000))`
ELAPSED_TIME=$(($END_TIME - $START_TIME))
echo "[xsbench] elapsed time in milliseconds = "$ELAPSED_TIME >> $1
