#include <stdio.h>

int main(){
    FILE* fptr1;
    FILE* fptr2;

    char str[50];

    fptr1 = fopen("input.txt","r");
    fptr2 = fopen("output.txt","w");

    while(1){
        if(feof(fptr1)){
            break;
        }
        fgets(str,50,fptr1);
        fputs(str,fptr2);
    }
    fclose(fptr1);
    fclose(fptr2);
    return 0;
}