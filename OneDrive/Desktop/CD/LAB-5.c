#include <stdio.h>
#include <string.h>

#define TSIZE 128

int parsingTable[100][TSIZE];
char terminals[TSIZE];
char nonterminals[26];

struct Production {
    char productionStr[100];
    int length;
} productions[20];

int numProductions;

char first[26][TSIZE];
char follow[26][TSIZE];
char firstOfRHS[100][TSIZE];

int isNonTerminal(char c) {
    return c >= 'A' && c <= 'Z';
}

void readGrammarFromFile() {
    FILE* filePtr;
    filePtr = fopen("grammar.txt", "r");
    char buffer[255];
    int i;
    int j;

    printf("\n------- Context-Free Grammar -------\n");

    while (fgets(buffer, sizeof(buffer), filePtr)) {
        printf("%s", buffer);
        j = 0;
        nonterminals[buffer[0] - 'A'] = 1;

        for (i = 0; i < strlen(buffer) - 1; ++i) {
            if (buffer[i] == '|') {
                ++numProductions;
                productions[numProductions - 1].productionStr[j] = '\0';
                productions[numProductions - 1].length = j;
                productions[numProductions].productionStr[0] = productions[numProductions - 1].productionStr[0];
                productions[numProductions].productionStr[1] = productions[numProductions - 1].productionStr[1];
                productions[numProductions].productionStr[2] = productions[numProductions - 1].productionStr[2];
                j = 3;
            } else {
                productions[numProductions].productionStr[j] = buffer[i];
                ++j;
                if (!isNonTerminal(buffer[i]) && buffer[i] != '-' && buffer[i] != '>') {
                    terminals[buffer[i]] = 1;
                }
            }
        }
        productions[numProductions].length = j;
        ++numProductions;
    }
}

void addToFirstOfAtoFollowOfB(char A, char B) {
    int i;
    for (i = 0; i < TSIZE; ++i) {
        if (i != '^') {
            follow[B - 'A'][i] = follow[B - 'A'][i] || first[A - 'A'][i];
        }
    }
}

void addToFollowOfAtoFollowOfB(char A, char B) {
    int i;
    for (i = 0; i < TSIZE; ++i) {
        if (i != '^') {
            follow[B - 'A'][i] = follow[B - 'A'][i] || follow[A - 'A'][i];
        }
    }
}

void computeFollow() {
    int t = 0;
    int i, j, k, x;

    while (t++ < numProductions) {
        for (k = 0; k < 26; ++k) {
            if (!nonterminals[k]) continue;
            char nt = k + 'A';

            for (i = 0; i < numProductions; ++i) {
                for (j = 3; j < productions[i].length; ++j) {
                    if (nt == productions[i].productionStr[j]) {
                        for (x = j + 1; x < productions[i].length; ++x) {
                            char sc = productions[i].productionStr[x];
                            if (isNonTerminal(sc)) {
                                addToFirstOfAtoFollowOfB(sc, nt);
                                if (first[sc - 'A']['^'])
                                    continue;
                            } else {
                                follow[nt - 'A'][sc] = 1;
                            }
                            break;
                        }
                        if (x == productions[i].length)
                            addToFollowOfAtoFollowOfB(productions[i].productionStr[0], nt);
                    }
                }
            }
        }
    }
}

void addToFirstOfAtoFirstOfB(char A, char B) {
    int i;
    for (i = 0; i < TSIZE; ++i) {
        if (i != '^') {
            first[B - 'A'][i] = first[A - 'A'][i] || first[B - 'A'][i];
        }
    }
}

void computeFirst() {
    int i, j;
    int t = 0;

    while (t < numProductions) {
        for (i = 0; i < numProductions; ++i) {
            for (j = 3; j < productions[i].length; ++j) {
                char sc = productions[i].productionStr[j];
                if (isNonTerminal(sc)) {
                    addToFirstOfAtoFirstOfB(sc, productions[i].productionStr[0]);
                    if (first[sc - 'A']['^'])
                        continue;
                } else {
                    first[productions[i].productionStr[0] - 'A'][sc] = 1;
                }
                break;
            }
            if (j == productions[i].length)
                first[productions[i].productionStr[0] - 'A']['^'] = 1;
        }
        ++t;
    }
}

void addToFirstOfAtoFirstRHSOfB(char A, int B) {
    int i;
    for (i = 0; i < TSIZE; ++i) {
        if (i != '^') {
            firstOfRHS[B][i] = first[A - 'A'][i] || firstOfRHS[B][i];
        }
    }
}

void computeFirstRHS() {
    int i, j;
    int t = 0;

    while (t < numProductions) {
        for (i = 0; i < numProductions; ++i) {
            for (j = 3; j < productions[i].length; ++j) {
                char sc = productions[i].productionStr[j];
                if (isNonTerminal(sc)) {
                    addToFirstOfAtoFirstRHSOfB(sc, i);
                    if (first[sc - 'A']['^'])
                        continue;
                } else {
                    firstOfRHS[i][sc] = 1;
                }
                break;
            }
            if (j == productions[i].length)
                firstOfRHS[i]['^'] = 1;
        }
        ++t;
    }
}

int main() {
    readGrammarFromFile();
    follow[productions[0].productionStr[0] - 'A']['$'] = 1;
    computeFirst();
    computeFollow();
    computeFirstRHS();
    int i, j, k;

    printf("\n");

    for (i = 0; i < numProductions; ++i) {
        if (i == 0 || (productions[i - 1].productionStr[0] != productions[i].productionStr[0])) {
            char c = productions[i].productionStr[0];
            printf("FIRST OF %c: ", c);
            for (j = 0; j < TSIZE; ++j) {
                if (first[c - 'A'][j]) {
                    printf("%c ", j);
                }
            }
            printf("\n");
        }
    }

    printf("\n");

    for (i = 0; i < numProductions; ++i) {
        if (i == 0 || (productions[i - 1].productionStr[0] != productions[i].productionStr[0])) {
            char c = productions[i].productionStr[0];
            printf("FOLLOW OF %c: ", c);
            for (j = 0; j < TSIZE; ++j) {
                if (follow[c - 'A'][j]) {
                    printf("%c ", j);
                }
            }
            printf("\n");
        }
    }

    printf("\n");

    for (i = 0; i < numProductions; ++i) {
        printf("FIRST OF %s: ", productions[i].productionStr);
        for (j = 0; j < TSIZE; ++j) {
            if (firstOfRHS[i][j]) {
                printf("%c ", j);
            }
        }
        printf("\n");
    }

    terminals['$'] = 1;
    terminals['^'] = 0;

    printf("\n");
    printf("\n\t**************** LL(1) PARSING TABLE *******************\n");
    printf("\t--------------------------------------------------------\n");
    printf("%-10s", "");
    for (i = 0; i < TSIZE; ++i) {
        if (terminals[i]) printf("%-10c", i);
    }
    printf("\n");

    int p = 0;
    for (i = 0; i < numProductions; ++i) {
        if (i != 0 && (productions[i].productionStr[0] != productions[i - 1].productionStr[0]))
            p = p + 1;
        for (j = 0; j < TSIZE; ++j) {
            if (firstOfRHS[i][j] && j != '^') {
                parsingTable[p][j] = i + 1;
            } else if (firstOfRHS[i]['^']) {
                for (k = 0; k < TSIZE; ++k) {
                    if (follow[productions[i].productionStr[0] - 'A'][k]) {
                        parsingTable[p][k] = i + 1;
                    }
                }
            }
        }
    }

    k = 0;
    for (i = 0; i < numProductions; ++i) {
        if (i == 0 || (productions[i - 1].productionStr[0] != productions[i].productionStr[0])) {
            printf("%-10c", productions[i].productionStr[0]);
            for (j = 0; j < TSIZE; ++j) {
                if (parsingTable[k][j]) {
                    printf("%-10s", productions[parsingTable[k][j] - 1].productionStr);
                } else if (terminals[j]) {
                    printf("%-10s", "");
                }
            }
            ++k;
            printf("\n");
        }
    }

    return 0;
}
