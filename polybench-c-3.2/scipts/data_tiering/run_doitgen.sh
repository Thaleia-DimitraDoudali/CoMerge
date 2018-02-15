#/bin/sh

Usage="./run_doitgen.sh <output file>"

if [ $# -ne 1 ]; then
    echo $Usage
    exit 1
fi   

BENCH="
    ../linear-algebra/kernels/doitgen/doitgen_time_A
    ../linear-algebra/kernels/doitgen/doitgen_time_C4
    ../linear-algebra/kernels/doitgen/doitgen_time_sum
"

### Run all fast ###
echo "All fast" >> $1
numactl --cpunodebind=0 --membind=0 ../utilities/time_benchmark.sh ../linear-algebra/kernels/doitgen/doitgen_time 2>>$1

### Run placement ###
for b in $BENCH
do
    echo $b >> $1
    numactl --cpunodebind=0 --membind=0 ../utilities/time_benchmark.sh $b 2>>$1
done

### Run all slow ###
echo "All slow" >> $1
numactl --cpunodebind=0 --membind=1 ../utilities/time_benchmark.sh ../linear-algebra/kernels/doitgen/doitgen_time 2>>$1
