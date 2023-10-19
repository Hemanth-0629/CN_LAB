#include <stdio.h>
#include <stdlib.h>

struct Process {
    int id;
    int aTime;
    int bTime;
    struct Process* nxt;
};

void push_process(struct Process** root, int id, int aTime, int bTime) {
    struct Process* new_process = (struct Process*)malloc(sizeof(struct Process));
    new_process->id = id;
    new_process->aTime = aTime;
    new_process->bTime = bTime;
    new_process->nxt = NULL;

    if (*root == NULL) {
        *root = new_process;
    } else {
        struct Process* current = *root;
        while (current->nxt) {
            current = current->nxt;
        }
        current->nxt = new_process;
    }
}

struct Process* find_min(struct Process** root, int c_t) {
    struct Process* current = *root;
    struct Process* prev = NULL;
    struct Process* min_process = *root;
    struct Process* prev_min = NULL;

    while (current) {
        if (current->aTime <= c_t && current->bTime < min_process->bTime) {
            min_process = current;
            prev_min = prev;
        }
        prev = current;
        current = current->nxt;
    }

    if (prev_min == NULL) {
        *root = min_process->nxt;
    } else {
        prev_min->nxt = min_process->nxt;
    }

    return min_process;
}

void sjf(struct Process* root) {
    int c_t = 0;
    int comp_time[10] = {0};
    int turnaround_time[10] = {0};
    int wait_time[10] = {0};
    int res_time[10] = {0};

    float total_wait_time = 0.0;
    float total_turnaround_time = 0.0;
    int num_processes = 0;

    while (root != NULL) {
        struct Process* c_p = find_min(&root, c_t);

        res_time[c_p->id] = c_t - c_p->aTime;
        comp_time[c_p->id] = c_t + c_p->bTime;
        turnaround_time[c_p->id] = comp_time[c_p->id] - c_p->aTime;
        wait_time[c_p->id] = turnaround_time[c_p->id] - c_p->bTime;

        total_wait_time += wait_time[c_p->id];
        total_turnaround_time += turnaround_time[c_p->id];

        c_t += c_p->bTime;
        num_processes++;
        free(c_p);
    }

    printf("\nProcess\tCT\tTAT\tWT\tRT\n");
    for (int i = 0; i < 10; i++) {
        if (comp_time[i] > 0) {
            printf("%d\t%d\t\t%d\t\t%d\t\t%d\n", i, comp_time[i], turnaround_time[i], wait_time[i], res_time[i]);
        }
    }

    printf("\nAverage WT: %.2f\n", total_wait_time / num_processes);
    printf("Average TAT: %.2f\n", total_turnaround_time / num_processes);
}

int main() {
    struct Process* root = NULL;
    int n;

    printf("Enter no of processes: ");
    scanf("%d", &n);

    for (int i = 0; i < n; i++) {
        int id, aTime, bTime;
        printf("Enter the ID of process %d: ", i+1);
        scanf("%d", &id);
        printf("Enter the Arrival Time: ");
        scanf("%d", &aTime);
        printf("Enter the Burst Time: ");
        scanf("%d", &bTime);
        push_process(&root, id, aTime, bTime);
    }

    sjf(root);

    return 0;
}