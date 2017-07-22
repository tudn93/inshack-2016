#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#define FLAG 1
#define KEY  2

int main(int argc, char *argv[])
{
        if(argc < 3)
        {       printf("usage : ./flag_gen <flag> <key>");
        }
        else
        {       int kl = strlen(argv[KEY]);
                int fl = strlen(argv[FLAG]);
                //puts(argv[FLAG]);
                //puts(argv[KEY]);
                int i;
                printf("FLAG ARRAY : ");
                for(i = 0; i < fl; ++i)
                {       printf("%#x, ", argv[FLAG][i]);
                }
                printf("\nKEY ARRAY : ");
                for(i = 0; i < kl; ++i)
                {       printf("%#x, ", argv[KEY][i]);
                }
        }
        puts("");
}
