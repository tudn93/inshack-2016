```
    xor(xor("test_encryption" + "\0"*5, b64decode(test_encryption.tar.out)), b64decode(flag.txt.out))
    Le mode de chiffrement Output Feedback genere un flux de données qui est xor avec le plaintext.
    Le flux de données dépend seulement de l'IV et de la clé AES.
    Donc si on chiffre deux fichiers avec la même clé et le même IV, le contenu des deux fichiers sera xor avec le même flux.
    Si on connait le contenu du deuxieme fichier (.tar donc c'est le filename du fichier contenu dans le tar puis des nullbytes),
    on peut retrouver le contenu du premier.
```