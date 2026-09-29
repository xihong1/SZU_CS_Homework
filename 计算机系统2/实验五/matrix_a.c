#include <windows.h>
#include <stdlib.h>
#include <stdio.h>

int main() {
    float *a, *b, *c, temp;
    long int i, j, k, size, m;
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

    for (i = 0; i < size; i++) {
        for (j = 0; j < size; j++) {
            c[i*size+j] = 0;
            for (k = 0; k < size; k++)
                c[i*size+j] += a[i*size+k] * b[k*size+j];
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