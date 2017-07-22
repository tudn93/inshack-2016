# Challenge Morser CTF 2016 (Stéganographie)

Ce challenge est extrêment simple lorsque l'on sait comment l'information est codée et encapsulée.

Le principe est simple un message est caché dans l'image, il a été encodé en morse et dissimulé dans les bits de poids faible de l'image.

Un simple script python suffira à décoder ce message. Le traitement d'image est inutile dans ce cas.

Petite difficulté supplémentaire afin de coder les caractères `.`, `-` et ` ` (espace), les deux bits de poids faible sont utilisés.  
