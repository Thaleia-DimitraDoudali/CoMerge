all: my_malloc atax 2mm 3mm bicg cholesky doitgen gemm gemver gesummv mvt symm syr2k syrk trisolv trmm durbin dynprog gramschmidt lu ludcmp correlation covariance floyd-warshall reg_detect adi fdtd-2d fdtd-apml jacobi-1d-imper jacobi-2d-imper seidel-2d

LIB = utilities/lib_my_malloc.a -lnuma

my_malloc:
	gcc -c utilities/my_malloc.c -o utilities/my_malloc.o
	ar rcs utilities/lib_my_malloc.a utilities/my_malloc.o

atax:
	gcc -O3 -I utilities -I linear-algebra/kernels/atax utilities/polybench.c linear-algebra/kernels/atax/atax.c -DPOLYBENCH_TIME -DEXTRALARGE_DATASET $(LIB) -o linear-algebra/kernels/atax/atax_time
2mm:
	gcc -O3 -I utilities -I linear-algebra/kernels/2mm utilities/polybench.c linear-algebra/kernels/2mm/2mm.c -DPOLYBENCH_TIME -DLARGE_DATASET $(LIB) -o linear-algebra/kernels/2mm/2mm_time
3mm:
	gcc -O3 -I utilities -I linear-algebra/kernels/3mm utilities/polybench.c linear-algebra/kernels/3mm/3mm.c -DPOLYBENCH_TIME -DLARGE_DATASET -o linear-algebra/kernels/3mm/3mm_time
bicg:
	gcc -O3 -I utilities -I linear-algebra/kernels/bicg utilities/polybench.c linear-algebra/kernels/bicg/bicg.c -DPOLYBENCH_TIME -DLARGE_DATASET $(LIB) -o linear-algebra/kernels/bicg/bicg_time
cholesky:
	gcc -O3 -I utilities -I linear-algebra/kernels/cholesky utilities/polybench.c linear-algebra/kernels/cholesky/cholesky.c -DPOLYBENCH_TIME -DEXTRALARGE_DATASET -o linear-algebra/kernels/cholesky/cholesky_time -lm
doitgen:
	gcc -O3 -I utilities -I linear-algebra/kernels/doitgen utilities/polybench.c linear-algebra/kernels/doitgen/doitgen.c -DPOLYBENCH_TIME -DLARGE_DATASET $(LIB) -o linear-algebra/kernels/doitgen/doitgen_time 
gemm:
	gcc -O3 -I utilities -I linear-algebra/kernels/gemm utilities/polybench.c linear-algebra/kernels/gemm/gemm.c -DPOLYBENCH_TIME -DLARGE_DATASET -o linear-algebra/kernels/gemm/gemm_time 
gemver:
	gcc -O3 -I utilities -I linear-algebra/kernels/gemver utilities/polybench.c linear-algebra/kernels/gemver/gemver.c -DPOLYBENCH_TIME -DEXTRALARGE_DATASET -o linear-algebra/kernels/gemver/gemver_time 
gesummv:
	gcc -O3 -I utilities -I linear-algebra/kernels/gesummv utilities/polybench.c linear-algebra/kernels/gesummv/gesummv.c -DPOLYBENCH_TIME -DEXTRALARGE_DATASET -o linear-algebra/kernels/gesummv/gesummv_time 
mvt:
	gcc -O3 -I utilities -I linear-algebra/kernels/mvt utilities/polybench.c linear-algebra/kernels/mvt/mvt.c -DPOLYBENCH_TIME -DEXTRALARGE_DATASET -o linear-algebra/kernels/mvt/mvt_time 
symm:
	gcc -O3 -I utilities -I linear-algebra/kernels/symm utilities/polybench.c linear-algebra/kernels/symm/symm.c -DPOLYBENCH_TIME -DLARGE_DATASET -o linear-algebra/kernels/symm/symm_time 
syr2k:
	gcc -O3 -I utilities -I linear-algebra/kernels/syr2k utilities/polybench.c linear-algebra/kernels/syr2k/syr2k.c -DPOLYBENCH_TIME -DLARGE_DATASET -o linear-algebra/kernels/syr2k/syr2k_time 
syrk:
	gcc -O3 -I utilities -I linear-algebra/kernels/syrk utilities/polybench.c linear-algebra/kernels/syrk/syrk.c -DPOLYBENCH_TIME -DLARGE_DATASET -o linear-algebra/kernels/syrk/syrk_time 
trisolv:
	gcc -O3 -I utilities -I linear-algebra/kernels/trisolv utilities/polybench.c linear-algebra/kernels/trisolv/trisolv.c -DPOLYBENCH_TIME -DEXTRALARGE_DATASET $(LIB) -o linear-algebra/kernels/trisolv/trisolv_time 
trmm:
	gcc -O3 -I utilities -I linear-algebra/kernels/trmm utilities/polybench.c linear-algebra/kernels/trmm/trmm.c -DPOLYBENCH_TIME -DEXTRALARGE_DATASET $(LIB) -o linear-algebra/kernels/trmm/trmm_time 
durbin:
	gcc -O3 -I utilities -I linear-algebra/solvers/durbin utilities/polybench.c linear-algebra/solvers/durbin/durbin.c -DPOLYBENCH_TIME -DEXTRALARGE_DATASET -o linear-algebra/solvers/durbin/durbin_time 
dynprog:
	gcc -O3 -I utilities -I linear-algebra/solvers/dynprog utilities/polybench.c linear-algebra/solvers/dynprog/dynprog.c -DPOLYBENCH_TIME -DLARGE_DATASET -o linear-algebra/solvers/dynprog/dynprog_time 
gramschmidt:
	gcc -O3 -I utilities -I linear-algebra/solvers/gramschmidt utilities/polybench.c linear-algebra/solvers/gramschmidt/gramschmidt.c -DPOLYBENCH_TIME -DLARGE_DATASET -o linear-algebra/solvers/gramschmidt/gramschmidt_time -lm
lu:
	gcc -O3 -I utilities -I linear-algebra/solvers/lu utilities/polybench.c linear-algebra/solvers/lu/lu.c -DPOLYBENCH_TIME -DLARGE_DATASET -o linear-algebra/solvers/lu/lu_time 
ludcmp:
	gcc -O3 -I utilities -I linear-algebra/solvers/ludcmp utilities/polybench.c linear-algebra/solvers/ludcmp/ludcmp.c -DPOLYBENCH_TIME -DLARGE_DATASET $(LIB) -o linear-algebra/solvers/ludcmp/ludcmp_time 
correlation:
	gcc -O3 -I utilities -I datamining/correlation utilities/polybench.c datamining/correlation/correlation.c -DPOLYBENCH_TIME -DEXTRALARGE_DATASET -o datamining/correlation/correlation_time -lm
covariance:
	gcc -O3 -I utilities -I datamining/covariance utilities/polybench.c datamining/covariance/covariance.c -DPOLYBENCH_TIME -DMEDIUM_DATASET $(LIB) -o datamining/covariance/covariance_time 
floyd-warshall:
	gcc -O3 -I utilities -I medley/floyd-warshall utilities/polybench.c medley/floyd-warshall/floyd-warshall.c -DPOLYBENCH_TIME -DEXTRALARGE_DATASET -o medley/floyd-warshall/floyd-warshall_time
reg_detect:
	gcc -O3 -I utilities -I medley/reg_detect utilities/polybench.c medley/reg_detect/reg_detect.c -DPOLYBENCH_TIME -DLARGE_DATASET -o medley/reg_detect/reg_detect_time
adi:
	gcc -O3 -I utilities -I stencils/adi utilities/polybench.c stencils/adi/adi.c -DPOLYBENCH_TIME -DEXTRALARGE_DATASET $(LIB) -o stencils/adi/adi_time
fdtd-2d:
	gcc -O3 -I utilities -I stencils/fdtd-2d utilities/polybench.c stencils/fdtd-2d/fdtd-2d.c -DPOLYBENCH_TIME -DEXTRALARGE_DATASET $(LIB) -o stencils/fdtd-2d/fdtd-2d_time
fdtd-apml:
	gcc -O3 -I utilities -I stencils/fdtd-apml utilities/polybench.c stencils/fdtd-apml/fdtd-apml.c -DPOLYBENCH_TIME -DLARGE_DATASET -o stencils/fdtd-apml/fdtd-apml_time
jacobi-1d-imper:
	gcc -O3 -I utilities -I stencils/jacobi-1d-imper utilities/polybench.c stencils/jacobi-1d-imper/jacobi-1d-imper.c -DPOLYBENCH_TIME -DEXTRALARGE_DATASET -o stencils/jacobi-1d-imper/jacobi-1d-imper_time
jacobi-2d-imper:
	gcc -O3 -I utilities -I stencils/jacobi-2d-imper utilities/polybench.c stencils/jacobi-2d-imper/jacobi-2d-imper.c -DPOLYBENCH_TIME -DEXTRALARGE_DATASET $(LIB) -o stencils/jacobi-2d-imper/jacobi-2d-imper_time
seidel-2d:
	gcc -O3 -I utilities -I stencils/seidel-2d utilities/polybench.c stencils/seidel-2d/seidel-2d.c -DPOLYBENCH_TIME -DEXTRALARGE_DATASET -o stencils/seidel-2d/seidel-2d_time
