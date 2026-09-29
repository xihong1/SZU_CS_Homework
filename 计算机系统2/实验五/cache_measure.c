#include <windows.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#define NUM_ITERS 100

void test_cache_levels_random() {
    int i, iter;
    LARGE_INTEGER frequency, start, end;
    double elapsed;
    long long total = 0;

    QueryPerformanceFrequency(&frequency);

    printf("=== Cache Level Detection (Random Access) ===\n");
    printf("Size (KB) | Time (s) | Time/access (ns)\n");

    int sizes_kb[] = {4, 8, 16, 32, 48, 64, 96, 128, 192, 256, 384,
                      512, 768, 1024, 1536, 2048, 3072, 4096, 6144,
                      8192, 12288, 16384, 24576, 32768, 65536, 131072};
    int num_sizes = sizeof(sizes_kb) / sizeof(sizes_kb[0]);

    for (i = 0; i < num_sizes; i++) {
        int size = sizes_kb[i] * 1024;
        int num_accesses = size / 64;
        int *indices = (int*)malloc(num_accesses * sizeof(int));
        char *array = (char*)malloc(size);
        int j;

        if (!array || !indices) continue;

        memset(array, 1, size);

        for (j = 0; j < num_accesses; j++) indices[j] = j;
        for (j = num_accesses - 1; j > 0; j--) {
            int k = rand() % (j + 1);
            int tmp = indices[j]; indices[j] = indices[k]; indices[k] = tmp;
        }

        total = 0;
        QueryPerformanceCounter(&start);
        for (iter = 0; iter < NUM_ITERS; iter++)
            for (j = 0; j < num_accesses; j++)
                total += array[indices[j] * 64];
        QueryPerformanceCounter(&end);
        elapsed = (double)(end.QuadPart - start.QuadPart) / frequency.QuadPart;

        printf("%9d | %8.6f | %15.2f\n",
               sizes_kb[i], elapsed,
               (elapsed * 1e9) / (num_accesses * NUM_ITERS));

        free(array); free(indices);
    }
}

void test_cache_line_size() {
    int sizes[] = {16, 32, 48, 64, 80, 96, 128, 256, 512, 1024, 2048, 4096};
    int s, i, iter;
    LARGE_INTEGER frequency, start, end;
    long long total = 0;

    QueryPerformanceFrequency(&frequency);

    printf("=== Cache Line Size Test (Stride) ===\n");
    printf("Stride (B) | Time (s)\n");

    for (s = 0; s < sizeof(sizes)/sizeof(sizes[0]); s++) {
        int stride = sizes[s];
        int array_size = 64 * 1024;
        char *array = (char*)malloc(array_size);

        if (!array) continue;

        memset(array, 1, array_size);

        QueryPerformanceCounter(&start);
        for (iter = 0; iter < 10000; iter++)
            for (i = 0; i < array_size; i += stride)
                total += array[i];
        QueryPerformanceCounter(&end);

        double elapsed = (double)(end.QuadPart - start.QuadPart) / frequency.QuadPart;
        printf("%10d | %8.6f\n", stride, elapsed);
        free(array);
    }

    printf("(total=%lld)\n", total);
}

int main() {
    printf("=== x86 Cache Measurement Tool ===\n");

    test_cache_levels_random();
    test_cache_line_size();

    printf("\nDone.\n");
    return 0;
}