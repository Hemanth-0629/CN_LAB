//Importing of libraries
#include <stdio.h>

int main(){
    FILE* fptr;
    char c;
    char str[50];
    fptr = fopen("input.txt","r");
    if(fptr == NULL){
        printf("Unable to open the file\n");
    }
 
    else{
        while(1){
            fgets(str,50,fptr);
            if(feof(fptr)){
                break;
            }
            else{
                printf("%s",str);
            }
        }
    }
}