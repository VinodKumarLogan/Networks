#include <stdio.h>     /* for printf */
#include <stdlib.h>    /* for exit */
#include <unistd.h>    /* for getopt */
int main (int argc, char **argv) {
    int c;
    int digit_optind = 0;
    int aopt = 0, bopt = 0;
    char *copt = 0, *dopt = 0;
    while ( (c = getopt(argc, argv, "ab:")) != -1) {
        switch (c) {
            case 'a':
            printf ("option a\n");
            aopt = atoi(optarg);
            break;
        case 'b':
            printf ("option b\n");
            bopt = atoi(optarg);
            break;
        default:
            printf ("Invalid Input");
        }
    }
    printf("%d",aopt+bopt);
}
