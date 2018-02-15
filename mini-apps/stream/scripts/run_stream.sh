#/bin/sh

export OMP_NUM_THREADS=4
BENCH="/home/thaleia/comerge/mini-apps/stream/stream"

START_TIME=`echo $(($(date +%s%N)/1000000))`
numactl --cpunodebind=0 --membind=0 $BENCH >> $1
END_TIME=`echo $(($(date +%s%N)/1000000))`
ELAPSED_TIME=$(($END_TIME - $START_TIME))
echo "[stream] elapsed time in milliseconds = "$ELAPSED_TIME >> $1
