#include<stdio.h>
#include<string.h>
#define TSIZE 128

int productionTable[100][TSIZE];
char terminal[TSIZE];
char nonterminal[26];

struct Production {
    char str[100];
    int len;
} productions[20];

int numProductions;

char first[26][TSIZE];
char follow[26][TSIZE];
char firstRHS[100][TSIZE];

int isNonTerminal(char c) {
    return c >= 'A' && c <= 'Z';
}

void readGrammarFromFile() {
    FILE* filePtr;
    filePtr = fopen("CFG_LAB-1.txt", "r");
    char buffer[255];
    int i;
    int j;
    while (fgets(buffer, sizeof(buffer), filePtr)) {
        printf("%s", buffer);
        j = 0;
        nonterminal[buffer[0] - 'A'] = 1;
        for (i = 0; i < strlen(buffer) - 1; ++i) {
            if (buffer[i] == '|') {
                ++numProductions;
                productions[numProductions - 1].str[j] = '\0';
                productions[numProductions - 1].len = j;
                productions[numProductions].str[0] = productions[numProductions - 1].str[0];
                productions[numProductions].str[1] = productions[numProductions - 1].str[1];
                productions[numProductions].str[2] = productions[numProductions - 1].str[2];
                j = 3;
            }
            else {
                productions[numProductions].str[j] = buffer[i];
                ++j;
                if (!isNonTerminal(buffer[i]) && buffer[i] != '-' && buffer[i] != '>') {
                    terminal[buffer[i]] = 1;
                }
            }
        }
        productions[numProductions].len = j;
        ++numProductions;
    }
}

void addToFirstAtoFollowB(char A, char B) {
    int i;
    for (i = 0; i < TSIZE; ++i) {
        if (i != '^')
            follow[B - 'A'][i] = follow[B - 'A'][i] || first[A - 'A'][i];
    }
}

void addToFollowAtoFollowB(char A, char B) {
    int i;
    for (i = 0; i < TSIZE; ++i) {
        if (i != '^')
            follow[B - 'A'][i] = follow[B - 'A'][i] || follow[A - 'A'][i];
    }
}

void calculateFollow() {
    int t = 0;
    int i, j, k, x;
    while (t++ < numProductions) {
        for (k = 0; k < 26; ++k) {
            if (!nonterminal[k])    continue;
            char nt = k + 'A';
            for (i = 0; i < numProductions; ++i) {
                for (j = 3; j < productions[i].len; ++j) {
                    if (nt == productions[i].str[j]) {
                        for (x = j + 1; x < productions[i].len; ++x) {
                            char sc = productions[i].str[x];
                            if (isNonTerminal(sc)) {
                                addToFirstAtoFollowB(sc, nt);
                                if (first[sc - 'A']['^'])
                                    continue;
                            }
                            else {
                                follow[nt - 'A'][sc] = 1;
                            }
                            break;
                        }
                        if (x == productions[i].len)
                            addToFollowAtoFollowB(productions[i].str[0], nt);
                    }
                }
            }
        }
    }
}

void addToFirstAtoFirstB(char A, char B) {
    int i;
    for (i = 0; i < TSIZE; ++i) {
        if (i != '^') {
            first[B - 'A'][i] = first[A - 'A'][i] || first[B - 'A'][i];
        }
    }
}

void calculateFirst() {
    int i, j;
    int t = 0;
    while (t < numProductions) {
        for (i = 0; i < numProductions; ++i) {
            for (j = 3; j < productions[i].len; ++j) {
                char sc = productions[i].str[j];
                if (isNonTerminal(sc)) {
                    addToFirstAtoFirstB(sc, productions[i].str[0]);
                    if (first[sc - 'A']['^'])
                        continue;
                }
                else {
                    first[productions[i].str[0] - 'A'][sc] = 1;
                }
                break;
            }
            if (j == productions[i].len)
                first[productions[i].str[0] - 'A']['^'] = 1;
        }
        ++t;
    }
}

void addToFirstAtoFirstRHSB(char A, int B) {
    int i;
    for (i = 0; i < TSIZE; ++i) {
        if (i != '^')
            firstRHS[B][i] = first[A - 'A'][i] || firstRHS[B][i];
    }
}

void calculateFirstRHS() {
    int i, j;
    int t = 0;
    while (t < numProductions) {
        for (i = 0; i < numProductions; ++i) {
            for (j = 3; j < productions[i].len; ++j) {
                char sc = productions[i].str[j];
                if (isNonTerminal(sc)) {
                    addToFirstAtoFirstRHSB(sc, i);
                    if (first[sc - 'A']['^'])
                        continue;
                }
                else {
                    firstRHS[i][sc] = 1;
                }
                break;
            }
            if (j == productions[i].len)
                firstRHS[i]['^'] = 1;
        }
        ++t;
    }
}

int main() {
    readGrammarFromFile();
    follow[productions[0].str[0] - 'A']['$'] = 1;
    calculateFirst();
    calculateFollow();
    calculateFirstRHS();
    int i, j, k;

    // Display first of each variable
    printf("\n");
    for (i = 0; i < numProductions; ++i) {
        if (i == 0 || (productions[i - 1].str[0] != productions[i].str[0])) {
            char c = productions[i].str[0];
            printf("FIRST OF %c: ", c);
            for (j = 0; j < TSIZE; ++j) {
                if (first[c - 'A'][j]) {
                    printf("%c ", j);
                }
            }
            printf("\n");
        }
    }

    // Display follow  of each variable
    printf("\n");
    for (i = 0; i < numProductions; ++i) {
        if (i == 0 || (productions[i - 1].str[0] != productions[i].str[0])) {
            char c = productions[i].str[0];
            printf("FOLLOW OF %c: ", c);
            for (j = 0; j < TSIZE; ++j) {
                if (follow[c - 'A'][j]) {
                    printf("%c ", j);
                }
            }
             printf("\n");
        }
    }
}





