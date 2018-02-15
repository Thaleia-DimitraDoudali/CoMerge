#/bin/sh

Usage="./run_ludcmp.sh <output file>"

if [ $# -ne 1 ]; then
    echo $Usage
    exit 1
fi   

bn="../linear-algebra/solvers/ludcmp/ludcmp_time"

BENCH="
    ../linear-algebra/solvers/ludcmp/ludcmp_time_A
    ../linear-algebra/solvers/ludcmp/ludcmp_time_b
    ../linear-algebra/solvers/ludcmp/ludcmp_time_x
    ../linear-algebra/solvers/ludcmp/ludcmp_time_y
"
### Run all fast ###
echo "All fast" >> $1
#numactl --cpunodebind=0 --membind=0 ../utilities/time_benchmark.sh $bn 2>>$1
numactl --cpunodebind=0 --membind=0 $bn 2>>$1

### Run placement ###
for b in $BENCH
do
    echo $b >> $1
    numactl --cpunodebind=0 --membind=0 $b 2>>$1
done

### Run all slow ###
echo "All slow" >> $1
numactl --cpunodebind=0 --membind=1 $bn 2>>$1
