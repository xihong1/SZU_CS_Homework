#include <windows.h>
#include <stdlib.h>
#include <stdio.h>

#define BLOCK_SIZE 64

int main() {
    float *a, *b, *c, temp;
    long int i, j, k, ii, jj, kk, size, m;
    LARGE_INTEGER frequency, start, end;
    double elapsedTime;

    QueryPerformanceFrequency(&frequency);

    printf("\tEnter size of square matrix: ");
    scanf("%ld", &size);

    m = size * size;
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

    QueryPerformanceCounter(&end);

    elapsedTime = (double)(end.QuadPart - start.QuadPart) / frequency.QuadPart;
    printf("Execution time = %.6f seconds\n", elapsedTime);

    free(a);
    free(b);
    free(c);

    return 0;
}