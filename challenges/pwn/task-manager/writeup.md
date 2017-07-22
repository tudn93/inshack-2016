```
    On peut allouer des taches admin et user. Si on supprime une tache, elle disparait de la liste mais on peut toujours y accèder (use after free).
    Du coup, si on alloue une tache user, on la supprime puis on alloue une tache admin, on a un lien user vers une tache admin (la tache admin prend la place en memoire de la tache user).
    On a deux tasks qui pointent vers la tache admin (la user et la admin), on peut donc modifier la tache admin.
    On peut utiliser le heap overflow sur la tache user pour ecrire l'adresse de la fonction de débug dans le pointeur de fonction.
    Et comme la tache est admin (referencé dans l'autre sens), on peut lancer la fonction de la tache en passant par la tache user.
    La fonction de debug est vulnérable : on peut changer le PATH et executer son propre fichier touch.
    Exploit joint dans ./sources/
```