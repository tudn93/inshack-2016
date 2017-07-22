#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

#define NUMROUNDS 32
#define FLAGROUNDS 16

// https://en.wikipedia.org/wiki/Treyfer

void init_timer(void) __attribute__ ((constructor));

void end_timer(void) __attribute__ ((destructor));

// big hint in Sbox
uint8_t Sbox[256] = {65, 108, 108, 32, 111, 112, 101, 114, 97, 116, 105, 111, 110, 115, 32, 97, 114, 101, 32, 98, 121, 116, 101, 45, 111, 114, 105, 101, 110, 116, 101, 100, 44, 32, 97, 110, 100, 32, 116, 104, 101, 114, 101, 32, 105, 115, 32, 97, 32, 115, 105, 110, 103, 108, 101, 32, 56, 195, 151, 56, 98, 105, 116, 32, 83, 45, 98, 111, 120, 46, 32, 73, 110, 32, 101, 97, 99, 104, 32, 114, 111, 117, 110, 100, 44, 32, 101, 97, 99, 104, 32, 98, 121, 116, 101, 32, 104, 97, 115, 32, 97, 100, 100, 101, 100, 32, 116, 111, 32, 105, 116, 32, 116, 104, 101, 32, 83, 45, 98, 111, 120, 32, 118, 97, 108, 117, 101, 32, 111, 102, 32, 116, 104, 101, 32, 115, 117, 109, 32, 111, 102, 32, 97, 32, 107, 101, 121, 32, 98, 121, 116, 101, 32, 97, 110, 100, 32, 116, 104, 101, 32, 112, 114, 101, 118, 105, 111, 117, 115, 32, 100, 97, 116, 97, 32, 98, 121, 116, 101, 44, 32, 116, 104, 101, 110, 32, 105, 116, 32, 105, 115, 32, 114, 111, 116, 97, 116, 101, 100, 32, 108, 101, 102, 116, 32, 111, 110, 101, 32, 98, 105, 116, 46, 32, 84, 104, 101, 32, 97, 108, 103, 111, 114, 105, 116, 104, 109, 32, 105, 115, 32, 101, 120, 116, 114, 101, 109, 101, 108, 121, 32, 115, 105, 109, 112, 108, 101, 46, 32, 73, 78, 83, 72, 65, 67, 75};

uint64_t timer;
uint64_t check = 0;

void win() {	
	printf("Congratz you got the flag !\n");
}

void loose() {
	printf("...\n");
}


void init_timer(void) {
	uint32_t lo, hi;
	asm ("rdtsc" : "=a"(lo), "=d"(hi));
	timer = lo | ((uint64_t)hi << 32);
	return;
}

void end_timer(void) {
	uint64_t timer2;
	uint32_t lo, hi;
	asm ("rdtsc" : "=a"(lo), "=d"(hi));
	timer2 = lo | ((uint64_t)hi << 32);
	
	// Anti debug
	// printf("%lx", (timer2 - timer));
	if ((timer2 - timer) > 0x500000) {
		printf("What ! Is your computer slow or are you debugging me ?!?");
		exit(0);
	}
	
	// Real check
	//printf("check : %llu", check);
	if (check == 0xb4d3eb0bbeb10494){
		win();
	}
}

uint8_t * crypt(uint8_t * plain)
{
    unsigned i;
    uint8_t t = plain[0];
	
    for (i = 0; i < 8 * NUMROUNDS; i++) {
        t += Sbox[249 + (i % 8)]; 						  					/* Add key */
		if ((i / 8) == FLAGROUNDS) {
			check |= ((uint64_t)plain[(i+1) % 8]) << (((i+1) % 8) * 8);		/* save 16 rounds cipher for real check */
		}
        t = Sbox[t] + plain[(i+1)%8];					  					/* sbox + plain */
        plain[(i+1) % 8] = t = ((t << 1) | (t >> 7));        				/* Rotate left 1 bit */
    }
	
	// return treyfer key to make memcmp == 0 impossible
	return Sbox + 249;
}

/*
	FOR DEBUG ONLY
	flag: FLAG{good_boy}
	Flag ciphered : 9404b1be0bebd3b4
	Flag : good_boy
	Fake flag ciphered : a92a5e9bdd976296
	Fake flag : bad_flag

void test_flag() {
	uint8_t text[9] = {'g', 'o', 'o', 'd', '_', 'b', 'o', 'y', 0};
	int r, i;
   
    uint8_t t = text[0];
	
	// treyfer encrypt 16 rounds flag
    for (i = 0; i < (8 * FLAGROUNDS); i++) {
        t += Sbox[249 + (i % 8)];
        t = Sbox[t] + text[(i+1)%8];
        text[(i+1) % 8] = t = ((t << 1) | (t >> 7));
    }
	
	printf("Flag ciphered : ");
	for (i=0; i < 8; i++) {
		printf ("%02x", text[i]);
	}
	printf("\n");
	
	// treyfer decrypt 16 rounds flag
	for (r=0; r < FLAGROUNDS; r++) {
		text[0] = (((text[0]) >> 1) | ((text[0]) << 7)) - Sbox[(Sbox[249 + 7] + text[7]) & 0xff];
		for (i = 7; i > 0; i--) {
			text[i] = (((text[i]) >> 1) | ((text[i]) << 7)) - Sbox[(Sbox[249 + (i - 1)] + text[(i - 1)]) & 0xff];
		}
	}
	
	printf("Flag : %s\n", text);
}

void test_fake_flag() {
	uint8_t text[9] = {'b', 'a', 'd', '_', 'f', 'l', 'a', 'g', 0};
	int r, i;
   
    uint8_t t = text[0];
	
	// treyfer encrypt 32 rounds flag
    for (i = 0; i < (8 * NUMROUNDS); i++) {
        t += Sbox[249 + (i % 8)];
        t = Sbox[t] + text[(i+1)%8];
        text[(i+1) % 8] = t = ((t << 1) | (t >> 7));
    }
	
	printf("Fake flag ciphered : ");
	for (i=0; i < 8; i++) {
		printf ("%02x", text[i]);
	}
	printf("\n");
	
	// treyfer decrypt 32 rounds flag
	for (r=0; r < NUMROUNDS; r++) {
		text[0] = (((text[0]) >> 1) | ((text[0]) << 7)) - Sbox[(Sbox[249 + 7] + text[7]) & 0xff];
		for (i = 7; i > 0; i--) {
			text[i] = (((text[i]) >> 1) | ((text[i]) << 7)) - Sbox[(Sbox[249 + (i - 1)] + text[(i - 1)]) & 0xff];
		}
	}
	
	printf("Fake flag : %s\n", text);
}
*/

int main(int argc, char *argv[]) {
	if (argc < 2) {
		printf("Error missing argument !\n");
		printf("%s input\n", argv[0]);
		exit(0);
	}
	
	/* 		TESTS
		test_flag();
		test_fake_flag();
	*/
	
	uint8_t fake_flag [8] = {0xa9, 0x2a, 0x5e, 0x9b, 0xdd, 0x97, 0x62, 0x96};

	if ((memcmp("FLAG{", argv[1], 5) == 0) && (strlen(argv[1]) == 14) && (argv[1][13] == '}') && (memcmp(crypt(argv[1] + 5), fake_flag, 8) == 0))
	{
		win();
	} else {
		loose();
	}
	return 0;
}