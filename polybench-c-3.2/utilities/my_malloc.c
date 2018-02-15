#include <numa.h>
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

#include "my_malloc.h"


void my_print_address(void *ptr, size_t size, char name[256]) {
    //Start address
    fprintf(stderr, "%s, %p, %ld\n", name, ptr, size);
}    

/*---------1D layout---------*/
void *my_malloc(size_t size, int slow_node, int place_on_slow, char name[256]) {

    void *res = NULL;
    if ((slow_node != -1) && (place_on_slow != 0)) {
        res = numa_alloc_onnode(size, slow_node);
    } else { // No slow memory
        res = malloc(size);
    }
    if (PRINT_ADDRESS == 1) my_print_address(res, size, name);
    return res;
}

void *my_calloc(size_t nmemb, size_t size, int slow_node, int place_on_slow, char name[256]) {

    void *res = NULL;
    if ((slow_node != -1) && (place_on_slow != 0)) {
        res = numa_alloc_onnode(nmemb * size, slow_node);
        memset(res, 0, nmemb * size);
    } else { // No slow memory
        res = calloc(nmemb, size);
    }        
    if (PRINT_ADDRESS == 1) my_print_address(res, nmemb*size, name);
    return res;

}    

void my_free(void *ptr, size_t size, int slow_node, int place_on_slow, char name[256]) {
    
    if ((slow_node != -1) && (place_on_slow != 0)) {
        numa_free(ptr, size);
    } else { // No slow memory
        free(ptr);
    }
    //if (PRINT_ADDRESS == 1) fprintf(stderr, "%s, %p, %u\n", name.c_str(), ptr, size);    
}

/*---------2D layout---------*/
void **my_malloc2D(size_t dim1, size_t type_size1, size_t dim2, size_t type_size2, int slow_node, int place_on_slow, char name[256]) {
    int i = 0;
    void **res = NULL;
    if ((slow_node != -1) && (place_on_slow != 0)) {
        res = numa_alloc_onnode(dim1*type_size1, slow_node);
        for (i = 0; i < dim1; i++) {
            res[i] = numa_alloc_onnode(dim2*type_size2, slow_node);
        }
    } else { // No slow memory
        res = malloc(dim1*type_size1);
        for (i = 0; i < dim1; i++) {
            res[i] = malloc(dim2*type_size2);
        }
    }
    int size = dim1*dim2*type_size2;
    if (PRINT_ADDRESS == 1) my_print_address(res, size, name);
    return res;
}

void my_free2D(void **ptr, size_t dim1, size_t type_size1, size_t dim2, size_t type_size2, int slow_node, int place_on_slow, char name[256]) {
    int i = 0;
    if ((slow_node != -1) && (place_on_slow != 0)) {
        for (i = 0; i < dim1; i++) {
            numa_free(ptr[i], dim2*type_size2);
        }
        numa_free(ptr, dim1*type_size1);
    } else { // No slow memory
        for (i = 0; i < dim1; i++) {
            free(ptr[i]);
        }
        free(ptr);
    }
} 
   
/*---------3D layout---------*/
void ***my_malloc3D(size_t dim1, size_t type_size1, size_t dim2, size_t type_size2, size_t dim3, size_t type_size3, int slow_node, int place_on_slow, char name[256]) {
    int i = 0, j = 0;
    void ***res = NULL;
    if ((slow_node != -1) && (place_on_slow != 0)) {
        res = (void ***) numa_alloc_onnode(dim1*type_size1, slow_node);
        for (i = 0; i < dim1; i++) {
            res[i] = (void **) numa_alloc_onnode(dim2*type_size2, slow_node);
            for (j = 0; j < dim2; j++) {
            	res[i][j] = (void *) numa_alloc_onnode(dim3*type_size3, slow_node);
	        }
        }
    } else { // No slow memory
        res = (void ***) malloc(dim1*type_size1);
        for (i = 0; i < dim1; i++) {
            res[i] = (void **) malloc(dim2*type_size2);
            for (j = 0; j < dim2; j++) {
            	res[i][j] = (void *) malloc(dim3*type_size3);
	        }
        }
    }
    //if (PRINT_ADDRESS == 1) my_print_address(res, dim1*dim2*dim3*type_size1*type_size2*type_size3, name);
    if (PRINT_ADDRESS == 1) my_print_address(res, dim1*type_size1 + dim1*dim2*type_size2 + dim1*dim2*dim3*type_size3, name);
    return res;
}

void my_free3D(void ***ptr, size_t dim1, size_t type_size1, size_t dim2, size_t type_size2, size_t dim3, size_t type_size3, int slow_node, int place_on_slow, char name[256]) {
    int i = 0, j = 0;
    if ((slow_node != -1) && (place_on_slow != 0)) {
        for (i = 0; i < dim1; i++) {
            for (j = 0; j < dim2; j++) {
            	numa_free(ptr[i][j], dim3*type_size3);
            }
            numa_free(ptr[i], dim2*type_size2);
	    }
        numa_free(ptr, dim1*type_size1);
    } else { // No slow memory
        for (i = 0; i < dim1; i++) {
            for (j = 0; j < dim2; j++) {
            	free(ptr[i][j]);
            }
            free(ptr[i]);
	    }
        free(ptr);
    }
} 
