```
    ./encoder encode $(python -c "print 'a'*48+'bash'.decode('base64')")
    OpenSSL rajoute les sauts de ligne si la sortie est trop grande donc on a une injection bash.
```