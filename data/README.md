Applications used and data input sizes:
- Polybench/C benchmark suite [Version 3.2] (http://web.cse.ohio-state.edu/~pouchet.2/software/polybench/)
```
./atax -NX 15000 -NY 15000 [make -DEXTRALARGE_DATASET]
./2mm -NI 4000 -NJ 4000 -NK 4000 -NL 4000 [make -DLARGE_DATASET]
./3mm -NI 4000 -NJ 4000 -NK 4000 -NL 4000 [make -DLARGE_DATASET]
./bicg -NX 13000 -NY 13000 [make -DLARGE_DATASET]
./cholesky -N 4000 [make -DEXTRALARGE_DATASET]
./doitgen -NQ 512 -NR 256 -NP 256 [make -DLARGE_DATASET]
./gemm -NI 2000 -NJ 2000 -NK 2000 [make -DLARGE_DATASET]
./gemver -N 15000 [make -DEXTRALARGE_DATASET]
./gesummv-N 10000 [make -DEXTRALARGE_DATASET]
./mvt -N 15000 [make -DEXTRALARGE_DATASET]
./symm -NI 2000 -NJ 2000 [make -DLARGE_DATASET]
./syr2k -NI 2000 -NJ 2000 [make -DLARGE_DATASET]
./syrk -NI 2000 -NJ 2000 [make -DLARGE_DATASET]
./trisolv -N 15000 [make -DEXTRALARGE_DATASET]
./trmm -NI 4000 [make -DEXTRALARGE_DATASET]
./durbin -N 10000 [make -DEXTRALARGE_DATASET]
./dynprog -TSTEPS 1000 -LENGTH 400 [make -DLARGE_DATASET]
./gramschmidt -NI 2000 -NJ 2000 [make -DLARGE_DATASET]
./lu -N 8000 [make -DLARGE_DATASET]
./ludcmp -N 8000 [make -DLARGE_DATASET]
./correlation -N 3000 -M 3000 [make -DEXTRALARGE_DATASET]
./covariance -N 1800 -M 1800 [make -DSTANDARD_DATASET]
./floyd-warshall -N 4000 [make -DEXTRALARGE_DATASET]
./reg_detect -NITER 1000 -LENGTH 5000 -MAXGRID 100 [make -DLARGE_DATASET]
./adi -TSTEPS 50 -N 8000 [make -DEXTRALARGE_DATASET]
./fdtd-2d -TMAX 100 -NX 8000 -NY 8000 [make -DEXTRALARGE_DATASET]
./fdtd-ampl -CZ 256 -CYM 256 -CXM 256 [make -DLARGE_DATASET]
./jacobi-1d -N 10000000 -TSTEPS 1000 [make -DEXTRALARGE_DATASET]
./jacovi-2d -N 8000 -TSTEPS 100 [make -DEXTRALARGE_DATASET]
./seidel-2d -N 5000 -TSTEPS 100 [make -DEXTRALARGE_DATASET]
```
- 3 CORAL mini-apps [STREAM, CLOMP, XSBench] (https://asc.llnl.gov/CORAL-benchmarks/)
```
./stream -N 70000000 -NTIMES 50
./clomp 4 1 64000 640 32 1 100 
./XSBench -s large -t 4 -g 2000 -l 50000000
```


