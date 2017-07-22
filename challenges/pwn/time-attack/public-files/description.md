# Time attack

Jay is a hardcore hacker. But this morning, after a 2 days long hacking contest, he can't figure out what's wrong about a simple binary. Will you help this sleepwalking hacker to find what's going on with this binary ? 

He left this note for you :
```c
int main(int argc, char **argv)
{
    printf("Challenge accepted ? [y/n]");
    string challenge_accepted;
    getline(cin, challenge_accepted);
    if( ! challenge_accepted.compare("y")) {    
        printf("Amazing, then goto ssh://time_attack@ctf.insecurity-insa.fr"); // the password is : time_attack
     } else { 
        printf("I'm so sad...");
    }
    return 0;
}
```
