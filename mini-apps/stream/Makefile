all: my_malloc stream

LIBS = lib_my_malloc.a -lnuma -fopenmp

my_malloc:
	gcc -c my_malloc.c -o my_malloc.o
	ar rcs lib_my_malloc.a my_malloc.o
stream:
	gcc -O3 stream_omp_v1.0.c -o stream $(LIBS)
clean:
	rm stream *.a *.o
