#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>

int main()
{
	setreuid(geteuid(), geteuid());
	system("SCRIPT_PATH_IN_JAIL");
	return 0;
}
