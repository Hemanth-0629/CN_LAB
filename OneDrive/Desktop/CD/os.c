#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int globalArray[5];

void updateArray(int value) {
    for (int i = 0; i < 5; i++) {
        globalArray[i] += value;
    }
}

int findMin() {
    int min = globalArray[0];
    for (int i = 1; i < 5; i++) {
        if (globalArray[i] < min) {
            min = globalArray[i];
        }
    }
    return min;
}

int findMax() {
    int max = globalArray[0];
    for (int i = 1; i < 5; i++) {
        if (globalArray[i] > max) {
            max = globalArray[i];
        }
    }
    return max;
}

int main() {
    pid_t pid;
    int minValue, maxValue;

    // Taking input from the user
    printf("Enter 5 integers for the global array:\n");
    for (int i = 0; i < 5; i++) {
        scanf("%d", &globalArray[i]);
    }

    pid = fork();

    if (pid < 0) {
        fprintf(stderr, "Fork failed\n");
        return 1;
    } else if (pid == 0) {
        // Child process
        updateArray(2);

        printf("Child Process:\n");
        for (int i = 0; i < 5; i++) {
            printf("Element: %d, Address: %p\n", globalArray[i], &globalArray[i]);
        }

        maxValue = findMax();
        printf("Maximum Element after adding 2: %d\n", maxValue);

        printf("Child Process ID: %d, Parent Process ID: %d\n", getpid(), getppid());
    } else {
        // Parent process
        updateArray(-3);

        printf("Parent Process:\n");
        for (int i = 0; i < 5; i++) {
            printf("Element: %d, Address: %p\n", globalArray[i], &globalArray[i]);
        }

        minValue = findMin();
        printf("Minimum Element after subtracting 3: %d\n", minValue);

        printf("Parent Process ID: %d, Child Process ID: %d\n", getpid(), pid);
    }

    return 0;
}
