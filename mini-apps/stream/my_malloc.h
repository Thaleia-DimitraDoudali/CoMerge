#ifndef MY_MALLOC_H_
#define MY_MALLOC_H_

#define PRINT_ADDRESS 0

/*---------1D layout---------*/
void *my_malloc(size_t size, int slow_node, int place_on_slow, char name[256]);
void *my_calloc(size_t nmemb, size_t size, int slow_node, int place_on_slow, char name[256]);
void my_free(void *ptr, size_t size, int slow_node, int place_on_slow, char name[256]);

/*---------2D layout---------*/
void **my_malloc2D(size_t dim1, size_t type_size1, size_t dim2, size_t type_size2, int slow_node, int place_on_slow, char name[256]);
void my_free2D(void **ptr, size_t dim1, size_t type_size1, size_t dim2, size_t type_size2, int slow_node, int place_on_slow, char name[256]);

/*---------3D layout---------*/
void ***my_malloc3D(size_t dim1, size_t type_size1, size_t dim2, size_t type_size2, size_t dim3, size_t type_size3, int slow_node, int place_on_slow, char name[256]);
void my_free3D(void ***ptr, size_t dim1, size_t type_size1, size_t dim2, size_t type_size2, size_t dim3, size_t type_size3, int slow_node, int place_on_slow, char name[256]);
#endif /* MY_MALLOC_H_ */

