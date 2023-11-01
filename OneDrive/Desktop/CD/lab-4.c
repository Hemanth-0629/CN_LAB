#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>

char* input_string;
int current_index = 0;

char get_next_token() {
    return input_string[current_index++];
}

void report_error() {
    printf("Error: Invalid token\n");
    exit(1);
}

bool parse_A(); // Forward declaration
bool parse_B(); // Forward declaration

bool parse_S() {
    char token = get_next_token();
    if (token == 'a') {
        if (parse_A() && parse_S()) {
            return true;
        }
    } else if (token == 'c') {
        return true;
    } else {
        report_error();
    }
    return false;
}

bool parse_A() {
    char token = get_next_token();
    if (token == 'b') {
        if (get_next_token() == 'a') {
            return true;
        } else {
            report_error();
        }
    } else if (token == 'a' || token == 'c') {
        if (parse_S() && parse_B()) {
            return true;
        }
    } else {
        report_error();
    }
    return false;
}

bool parse_B() {
    char token = get_next_token();
    if (token == 'b') {
        if (parse_A()) {
            return true;
        }
    } else if (token == 'a' || token == 'c') {
        if (parse_S()) {
            return true;
        }
    } else {
        report_error();
    }
    return false;
}

int main() {
    input_string = "abac$";

    if (parse_S() && input_string[current_index] == '$') {
        printf("Accepted\n");
    } else {
        printf("Rejected\n");
    }

    return 0;
}
