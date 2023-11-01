#include <stdio.h>

int main(){
    FILE* fptr;

    fptr = fopen("output.txt","a");
   
    char str[50];
    printf("Enter the setence you wanna append: ");
    scanf("%s",str);

    fputs(str,fptr);
    fclose(fptr);
    return 0;
}