/**
 * trisolv.c: This file is part of the PolyBench/C 3.2 test suite.
 *
 *
 * Contact: Louis-Noel Pouchet <pouchet@cse.ohio-state.edu>
 * Web address: http://polybench.sourceforge.net
 */
#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <math.h>

/* Include polybench common header. */
#include <polybench.h>

/* Include benchmark-specific header. */
/* Default data type is double, default size is 4000. */
#include "trisolv.h"
#include "my_malloc.h"


/* Array initialization. */
static
void init_array(int n,
/*		DATA_TYPE POLYBENCH_2D(A,N,N,n,n),
		DATA_TYPE POLYBENCH_1D(x,N,n),
		DATA_TYPE POLYBENCH_1D(c,N,n))*/
            DATA_TYPE **A,
            DATA_TYPE *x,
            DATA_TYPE *c)
{
  int i, j;

  for (i = 0; i < n; i++)
    {
      c[i] = x[i] = ((DATA_TYPE) i) / n;
      for (j = 0; j < n; j++)
	A[i][j] = ((DATA_TYPE) i*j) / n;
    }
}


/* DCE code. Must scan the entire live-out data.
   Can be used also to check the correctness of the output. */
static
void print_array(int n,
		 DATA_TYPE POLYBENCH_1D(x,N,n))

{
  int i;

  for (i = 0; i < n; i++) {
    fprintf (stderr, DATA_PRINTF_MODIFIER, x[i]);
    if (i % 20 == 0) fprintf (stderr, "\n");
  }
}


/* Main computational kernel. The whole function will be timed,
   including the call and return. */
static
void kernel_trisolv(int n,
            DATA_TYPE **A,
            DATA_TYPE *x,
            DATA_TYPE *c)
	/*	    DATA_TYPE POLYBENCH_2D(A,N,N,n,n),
		    DATA_TYPE POLYBENCH_1D(x,N,n),
		    DATA_TYPE POLYBENCH_1D(c,N,n))*/
{
  int i, j;

#pragma scop
  for (i = 0; i < _PB_N; i++)
    {
      x[i] = c[i];
      for (j = 0; j <= i - 1; j++)
        x[i] = x[i] - A[i][j] * x[j];
      x[i] = x[i] / A[i][i];
    }
#pragma endscop

}


int main(int argc, char** argv)
{
  /* Retrieve problem size. */
  int n = N;

  /* Variable declaration/allocation. */
  /*POLYBENCH_2D_ARRAY_DECL(A, DATA_TYPE, N, N, n, n);
  POLYBENCH_1D_ARRAY_DECL(x, DATA_TYPE, N, n);
  POLYBENCH_1D_ARRAY_DECL(c, DATA_TYPE, N, n);
*/
  DATA_TYPE **A = (DATA_TYPE **) my_malloc2D (N, sizeof(DATA_TYPE *), N, sizeof(DATA_TYPE), 1, 1, "A");
  DATA_TYPE *x = (DATA_TYPE *) my_malloc (N*sizeof(DATA_TYPE), 1, 1, "x");
  DATA_TYPE *c = (DATA_TYPE *) my_malloc (N*sizeof(DATA_TYPE), 0, 1, "c");

  /* Initialize array(s). */
  //init_array (n, POLYBENCH_ARRAY(A), POLYBENCH_ARRAY(x), POLYBENCH_ARRAY(c));
  init_array (n, A, x, c);

  /* Start timer. */
  polybench_start_instruments;

  /* Run kernel. */
  //kernel_trisolv (n, POLYBENCH_ARRAY(A), POLYBENCH_ARRAY(x), POLYBENCH_ARRAY(c));
  kernel_trisolv (n, A, x, c);

  /* Stop and print timer. */
  polybench_stop_instruments;
  polybench_print_instruments;

  /* Prevent dead-code elimination. All live-out data must be printed
     by the function call in argument. */
//  polybench_prevent_dce(print_array(n, POLYBENCH_ARRAY(x)));

  /* Be clean. */
 // POLYBENCH_FREE_ARRAY(A);
 // POLYBENCH_FREE_ARRAY(x);
 // POLYBENCH_FREE_ARRAY(c);

  return 0;
}
