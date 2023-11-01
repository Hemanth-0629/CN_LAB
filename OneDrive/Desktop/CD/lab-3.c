#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

char *keywords[] = {
    "auto", "break", "case", "char", "const", "continue",
    "default", "do", "double", "else", "enum", "extern",
    "float", "for", "goto", "if", "int", "long", "register",
    "return", "short", "signed", "sizeof", "static",
    "struct", "switch", "typedef", "union",
    "unsigned", "void", "volatile", "while"
};

#define NUM_KEYWORDS (sizeof(keywords) / sizeof(keywords[0]))

int isKeyword(const char *word) {
    for (int i = 0; i < NUM_KEYWORDS; ++i) {
        if (strcmp(word, keywords[i]) == 0) {
            return 1;
        }
    }
    return 0;
}

int main(int argc, char *argv[]) {
    
    FILE* inputFile = fopen(argv[1], "r");
    FILE* outputFile = fopen("output.c", "w");
    char currentChar, nextChar;

    while ((currentChar = fgetc(inputFile)) != EOF) {
        if (currentChar == '/') {
            nextChar = fgetc(inputFile);
            if (nextChar == '/') {
                while ((currentChar = fgetc(inputFile)) != '\n' && currentChar != EOF);
            }
            else if (nextChar == '*') {
                while (!((currentChar = fgetc(inputFile)) == '*' && (nextChar = fgetc(inputFile)) == '/')) {
                    if (currentChar == EOF) {
                        printf("Error: Unclosed multi-line comment.\n");
                        return 1;
                    }
                }
            }
            else {
                fputc(currentChar, outputFile);
                fputc(nextChar, outputFile);
            }
        }
        else {
            fputc(currentChar, outputFile);
        }
    }

    fclose(inputFile);
    fclose(outputFile);

    int idCount = 0, keywordCount = 0, constCount = 0, operatorCount = 0, specialCharCount = 0, strCount = 0;
    FILE* ptr = fopen("output.c", "r");
    int c;
    char currentWord[100];
    int wordIndex = 0;

    while ((c = fgetc(ptr)) != EOF) {
        if (isalpha(c) || c == '_') {
            wordIndex = 0;
            currentWord[wordIndex++] = c;

            while ((c = fgetc(ptr)) != EOF && (isalnum(c) || c == '_')) {
                currentWord[wordIndex++] = c;
            }

            currentWord[wordIndex] = '\0';

            if (isKeyword(currentWord)) {
                printf("%s     -     keyword\n", currentWord);
                keywordCount++;
            } else {
                printf("%s     -     identifier\n", currentWord);
                idCount++;
            }
        }
        else if (isdigit(c)) {
            char numBuffer[20];
            numBuffer[0] = c;
            char ch;
            int i = 1;
            
            while (isdigit(ch = getc(ptr))) {
                if (ch == ' ' || !isdigit(ch)) {
                    break;
                }
                numBuffer[i] = ch;
                i++;
            }
            numBuffer[i] = '\0';
            
            printf("%s     -     constant\n", numBuffer);

            int isFloat = 0;
            wordIndex = 0;
            currentWord[wordIndex++] = c;

            while ((c = fgetc(ptr)) != EOF && (isdigit(c) || c == '.')) {
                if (c == '.') {
                    isFloat = 1;
                }
                currentWord[wordIndex++] = c;
            }

            currentWord[wordIndex] = '\0';

            if (isFloat) {
                constCount++;
            } else {
                constCount++;
            }
        }
        else if (c == '\"') {
            strCount++;
            char strBuffer[100];
            int i = 0;

            while ((c = fgetc(ptr)) != EOF && c != '\"') {
                strBuffer[i] = c;
                i++;
            }

            strBuffer[i] = '\0';
            printf("%s    -     string\n", strBuffer);
        }
        else if (c != ' ' && c != '\t' && c != '\n') {
            specialCharCount++;
            printf("%c     -     Special character\n", c);

            if (c == '+' || c == '-' || c == '*' || c == '/' || c == '%' || c == '=' || c == '<' || c == '>' || c == '&' || c == '|' || c == '!' || c == '^') {
                int nextChar = fgetc(ptr);
                if (nextChar == c || (nextChar == '=' && (c == '+' || c == '-' || c == '*' || c == '/' || c == '%' || c == '=' || c == '<' || c == '>' || c == '&' || c == '|' || c == '^'))) {
                    operatorCount++;
                    printf("%c    -     operator\n", c);
                } else {
                    ungetc(nextChar, ptr);
                }
            }
        }
    }

    fclose(ptr);

    printf(" Identifiers: %d\n", idCount);
    printf(" Keywords: %d\n", keywordCount);
    printf(" Constants: %d\n", constCount);
    printf(" Operators: %d\n", operatorCount);
    printf(" Special Characters: %d\n", specialCharCount);
    printf(" Strings: %d\n", strCount);

    return 0;
}
