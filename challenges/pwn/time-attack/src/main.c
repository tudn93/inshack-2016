#include <unistd.h>
#include <stdio.h>
#include <string.h>

#define SLEEP_DURATION 1

int _lib_if_sleep_OO(char c, int i) {
        int ret = 0;
        switch(i) {
                case 0: if(c == 's') {sleep(SLEEP_DURATION);ret=1;} break;
                case 1: if(c == 'l') {sleep(SLEEP_DURATION);ret=1;} break;
                case 2: if(c == 'e') {sleep(SLEEP_DURATION);ret=1;} break;
                case 3: if(c == 'e') {sleep(SLEEP_DURATION);ret=1;} break;
                case 4: if(c == 'p') {sleep(SLEEP_DURATION);ret=1;} break;
                case 5: if(c == '2') {sleep(SLEEP_DURATION);ret=1;} break;
                case 6: if(c == 'm') {sleep(SLEEP_DURATION);ret=1;} break;
                case 7: if(c == 'u') {sleep(SLEEP_DURATION);ret=1;} break;
                case 8: if(c == 'c') {sleep(SLEEP_DURATION);ret=1;} break;
                case 9: if(c == 'h') {sleep(SLEEP_DURATION);ret=1;} break;
                default: break;
        }
        return ret;
}
/*
void _lib_out_OO() {
        char k[] = {0x31, 0x4d, 0x50, 0x30, 0x53, 0x53, 0x31, 0x42, 0x4c, 0x33, 0x5f, 0x54, 0x4f, 0x5f, 0x47, 0x55, 0x33, 0x35, 0x35};
        char f[] = {0x46, 0x4c, 0x41, 0x47, 0x7b, 0x53, 0x6c, 0x33, 0x33, 0x70, 0x5f, 0x31, 0x35, 0x5f, 0x62, 0x41, 0x64, 0x5f, 0x31, 0x44, 0x33, 0x34, 0x7d};
        int c;
        for(c = 0; c < strlen(f); ++c) {
                printf("%#x, ", f[c]^k[c]); // GENERATION FLAG
                //putc(f[c]^k[c % strlen(k)], stdout);
        }
        putc('\n', stdout);
}
*/
void _lib_outf_00() {
	puts("Try again");
}

void _lib_usage() {
	puts("Usage : ./main <password>");
}

int main(int argc, char * argv[]) {
        if(argc < 2) { _lib_usage(); return -1; }
        int i, ctr;
        ctr = 0;
        for(i = 0; i < strlen(argv[1]); ++i) {
                if(_lib_if_sleep_OO(argv[1][i], i) == 1)
                { ctr++; }
                else
                { break; }
                //printf("ctr=%d\n", ctr); //DEBUG
                //fflush(stdout); //DEBUG
        }
        if(ctr == 10) {
            puts("FLAG{T1m3_g1v3s_A_l0t_0f_1nf0}");
            //_lib_out_OO();
        } else {
        	_lib_outf_00();
        }
        return 0;
}
