#/bin/sh

BENCH="/home/thaleia/comerge/mini-apps/clomp_v1.2/my_clomp 4 1 64000 640 32 1 100"

START_TIME=`echo $(($(date +%s%N)/1000000))`
numactl --cpunodebind=0 --membind=0 $BENCH >> $1
END_TIME=`echo $(($(date +%s%N)/1000000))`
ELAPSED_TIME=$(($END_TIME - $START_TIME))
echo "[clomp] elapsed time in milliseconds = "$ELAPSED_TIME >> $1
