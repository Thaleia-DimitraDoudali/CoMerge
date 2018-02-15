#/bin/sh

XSBENCH="/home/thaleia/comerge/mini-apps/XSBench/src/scripts/run_xsbench.sh"
CLOMP="/home/thaleia/comerge/mini-apps/clomp_v1.2/scripts/run_clomp.sh"
STREAM="/home/thaleia/comerge/mini-apps/stream/scripts/run_stream.sh"

for i in 1 2 3 4 
do
    $XSBENCH xsbench.out
done &

for i in 1 2
do
    $CLOMP clomp.out
done &

for i in 1 2 3 4 5
do
    $STREAM stream.out
done &
