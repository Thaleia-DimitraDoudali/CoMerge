#!/bin/sh

RESDIR="results_throttle_perf_stalls"
THROTL="1 3 5 7 9"

throttle() {
    cd ~/comerge/throttle/
    python throttlectrl.py -n 1 -f $1
    cd -
}    

## Run all fast -- reset throttle
throttle 1
./run_all.sh 0 ${RESDIR}/fast.res

for th in $THROTL
do   
    throttle $th 
    ./run_all.sh 1 ${RESDIR}/slow_${th}.res
done    
