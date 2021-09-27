pypher
======
Classical symmetric cryptography tool

Ciphers
-----------------
+ Affine
+ Atbash
+ Beaufort
+ Caesar
+ Substitution
+ Vigenère

Encodings
---------
+ Morse code
+ Leet speak
+ Word lengths as alphabetic indexes

Features
--------
+ Chained string manipulation (internal pipeline)
+ Additional string processing (reverse, toggle case, etc.)

Chains
------
Chains are algorithm identifiers hyphenated in the desired order. Algorithms which require parameters, such as most ciphers, must be followed by a colon and their respective arguments. Note that if `-d`, `--decrypt` is specified, the chain will be parsed in reverse.

Examples
--------
+ Reverse a string, encrypt it with the Vigenère cipher and translate it to leet speak

**Encryption**
```
pypher -c reverse-vigenere:passphrase-leet 'message'
```
Output: `795khld`

**Decryption**
```
pypher -d -c reverse-vigenere:passphrase-leet '795khld'
```
Output: `message`

+ For every line of `message.txt`, encrypt it with the Beaufort cipher, reverse it, encrypt it with the Affine cipher, reverse it and output it to `secret.txt`

**Encryption**
```
pypher -c beaufort:passphrase-reverse-affine:3,11-reverse -o secret.txt message.txt
```
secret.txt: `zqpn ge k jbrfzi dseilv`

**Decryption**
```
pypher -d -c beaufort:passphrase-reverse-affine:3,11-reverse -o message.txt secret.txt
```
message.txt: `this is a secret message`
