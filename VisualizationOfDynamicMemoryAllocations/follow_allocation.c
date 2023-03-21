#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main() {

    // Alocam un element de tip int
    int *first_allocation = malloc(1*sizeof(int));

    sleep(1);
    // Alocam un element de tip char
    char *second_allocation = malloc(1*sizeof(char));
    sleep(1);

    // Alocam un vector de int uri
    int *third_allocation = malloc(3*sizeof(int));


    sleep(1);
    free(first_allocation);

    free(second_allocation);
    sleep(1);
    free(third_allocation);

    return 0;
}