#include <windows.h>
#include <stdlib.h>
#include <stdio.h>

#define BLOCK_SIZE 64

void matrix_multiply_normal(float *a, float *b, float *c, long size) {
    long i, j, k;
    for (i = 0; i < size; i++) {
        for (j = 0; j < size; j++) {
            c[i*size+j] = 0;
            for (k = 0; k < size; k++)
                c[i*size+j] += a[i*size+k] * b[k*size+j];
        }
    }
}

void matrix_multiply_optimized(float *a, float *b, float *c, long size) {
    long i, j, k, ii, jj, kk;
    for (ii = 0; ii < size; ii += BLOCK_SIZE) {
        for (jj = 0; jj < size; jj += BLOCK_SIZE) {
            for (kk = 0; kk < size; kk += BLOCK_SIZE) {
                for (i = ii; i < ii + BLOCK_SIZE && i < size; i++) {
                    for (j = jj; j < jj + BLOCK_SIZE && j < size; j++) {
                        float sum = c[i*size+j];
                        for (k = kk; k < kk + BLOCK_SIZE && k < size; k++) {
                            sum += a[i*size+k] * b[k*size+j];
                        }
                        c[i*size+j] = sum;
                    }
                }
            }
        }
    }
}

int main(int argc, char *argv[]) {
    long size;
    long m;
    float *a, *b, *c;
    long i, j;
    LARGE_INTEGER frequency, start, end;
    double elapsed_normal, elapsed_optimized;
    
    if (argc < 2) {
        printf("Usage: %s <matrix_size>\n", argv[0]);
        return 1;
    }
    
    size = atol(argv[1]);
    m = size * size;
    
    QueryPerformanceFrequency(&frequency);
    
    a = (float*)malloc(sizeof(float) * m);
    b = (float*)malloc(sizeof(float) * m);
    c = (float*)malloc(sizeof(float) * m);
    
    for (i = 0; i < size; i++) {
        for (j = 0; j < size; j++) {
            a[i*size+j] = (float)(rand() % 1000 / 100.0);
            b[i*size+j] = (float)(rand() % 1000 / 100.0);
        }
    }
    
    QueryPerformanceCounter(&start);
    matrix_multiply_normal(a, b, c, size);
    QueryPerformanceCounter(&end);
    elapsed_normal = (double)(end.QuadPart - start.QuadPart) / frequency.QuadPart;
    
    for (i = 0; i < m; i++) c[i] = 0;
    
    QueryPerformanceCounter(&start);
    matrix_multiply_optimized(a, b, c, size);
    QueryPerformanceCounter(&end);
    elapsed_optimized = (double)(end.QuadPart - start.QuadPart) / frequency.QuadPart;
    
    printf("%ld,%.6f,%.6f,%.2f\n", size, elapsed_normal, elapsed_optimized, elapsed_normal / elapsed_optimized);
    
    free(a);
    free(b);
    free(c);
    
    return 0;
}