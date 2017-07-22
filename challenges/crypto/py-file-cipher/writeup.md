```
Ce challenge consiste à retrouver un flag dans un dossier partagé par plusieurs utilisateurs (Alice et Bob) qui utilisent un script python
pour chiffrer leurs fichiers. L'algorithme de chiffrement symétrique utilisé est simple et il suffira de décompiler le fichier 
cipherfs avec UnPyc pour retrouver les opérations qui sont effectuées sur les octets de chaque fichier.

Deux utilisateurs seront présents dont un qui est en réalité le développeur (Bob) du script et qui a oublié de désactiver les logs. Son mot de passe peut donc être retrouvé en clair dans ces logs.

Le fichier cipherfs.py n'existera pas mais sa version compilée (.pyc) sera présente et désassemblable.

Il suffira ensuite d'aller chercher le flag dans le dossier d'un autre utilisateur (Alice) en retrouvant le mot de passe de ce dernier dans un echange de mails chiffrés par le développeur peu consciencieux.
```
