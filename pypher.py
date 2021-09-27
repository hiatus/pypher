#!/usr/bin/env python3

import sys

from os import path

# Local imports
import cipher


line = ''

chain = []

encrypt = True

file_in  = sys.stdin
file_out = sys.stdout

# {element:list of types of the expected arguments}
chain_elements = {
    'upper':[], 'lower':[], 'reverse':[], 'toggle':[], 'morse':[], 'leet':[],
    'freq':[], 'atbash':[], 'caesar':[int], 'vigenere':[str], 'beaufort':[str],
    'affine':[int, int], 'substitution':[str]
}

def_alpha = 'abcdefghijklmnopqrstuvwxyz'

base_banner = '''\
pypher [options] [file[s] | message]..

    -h, --help                 : this
    -d, --decrypt              : decrypt instead of encrypting

    -a, --alpha [str]          : set a different internal alphabet
    -c, --chain [str[-str]..]  : ordered list of ciphers/algorithms

    Notes
        + Use '--help' for more information
        + Only alphabet characters are encrypted/decrypted
        + The default alphabet is 'abcdefghijklmnopqrstuvwxyz'
        + When [file[s] | message] is not given, stdin is assumed
        + Pypher works on a line basis; the full chain is applied
          to each of the input lines
'''

full_banner = base_banner + '''

    Chain syntax
        + Chains are algorithm  identifiers  hyphenated in the  desired order.
          Algorithms which require parameters,  such as most ciphers,  must be
          followed by a colon and their  respective arguments.  Note that,  if
          '-d', '--decrypt' is specified, the chain will be parsed in reverse.

        Examples: 'reverse-leet', 'caesar:13', 'vigenere:passphrase-affine:3,11'


    Ciphers
        atbash              : no arguments
        caesar:[int]        : use int as shift
        vigenere:[str]      : use str as passphrase
        beaufort:[str]      : use str as passphrase
        substitution:[str]  : use str as translation alphabet
        affine:[int1,int2]  : use int1 as additive and int2 as multiplier


    Encodings
        morse  : morse code
        freq   : use length of words as alphabet index for each character
        leet   : substitution with default alphabet '48cd3f9h1jklmn0pqr57uvwxy2'

        Notes
            + '.' is used as character on 'freq' during encryption
            + ' ' is translated to or from '/' on 'morse' and 'freq'
            + All characters are treated as lower case on 'morse' and 'freq'


    General string manipulation
        toggle     : toggle case of each line character
        upper      : make all line characters upper case
        lower      : make all line characters lower case
        reverse    : reverse line characters ('input string' -> 'gnirts tupni')


    Examples
        + Encrypt a message using the Vigenère cipher
            pypher -c vigenere:secretpassword 'Hello, world'

            Note that separating 'Hello,' and 'world' generates 'Helloworld'

        + Encrypt and reverse each line of a text file using the Caesar cipher
            pypher -c caesar:15-reverse filename
'''

def _close_io():
    if file_in != sys.stdin:
        file_in.close()

    if file_out != sys.stdout:
        file_in.close()

    sys.exit(0)


def parse_chain(s):
    chain = []
    elements = [ss.strip() for ss in s.split('-')]

    for e in elements:
        e = e.split(':')

        if not e[0]:
            continue

        if e[0] not in chain_elements:
            raise ValueError("invalid chain element: '%s'" % e[0])
            exit(1)

        alg = e[0]
        chain_element_args = chain_elements.get(alg)

        args = [se.strip() for se in e[1].split(',')] if len(e) > 1 else []

        if len(args) != len(chain_element_args):
            raise ValueError("invalid number of arguments for '%s'" % alg)

        for i in range(len(chain_element_args)):
            try:
                args[i] = chain_element_args[i](args[i])

            except Exception:
                raise ValueError("invalid argument types for '%s'" % alg)

        chain.append(tuple([alg, args]))

    return tuple(chain) if encrypt else tuple(chain[::-1])


def apply_chain(s, chain):
    for alg, args in chain:
        crypter = None

        # Text manipulations
        if   alg == 'lower':   s = s.lower()
        elif alg == 'upper':   s = s.upper()
        elif alg == 'reverse': s = s[::-1]
        elif alg == 'toggle':  s = cipher.toggle(s)

        # Encodings
        elif alg  ==  'morse': s = cipher.morse(s, encrypt = encrypt)
        elif 'leet' in alg:    s = cipher.leet(s, def_alpha, encrypt = encrypt)
        elif alg  ==  'freq':  s = cipher.frequency_as_index(s, def_alpha,
                                                             encrypt = encrypt)

        # Ciphers
        elif alg == 'affine':
            crypter = cipher.Affine(args[0], args[1], def_alpha)
        elif alg == 'atbash':
            crypter = cipher.Atbash(def_alpha)
        elif alg == 'autokey':
            crypter = cipher.AutoKey(args[0], def_alpha)
        elif alg == 'beaufort':
            crypter = cipher.Beaufort(args[0], def_alpha)
        elif alg == 'caesar':
            crypter = cipher.Caesar(args[0], def_alpha)
        elif alg == 'substitution':
            crypter = cipher.SimpleSubstitution(args[0], args[1], def_alpha)
        elif alg == 'vigenere':
            crypter = cipher.Vigenere(args[0], def_alpha)
        else:
            raise ValueError("unexpected chain algorithm: '%s'" % alg)

        if crypter:
            s = crypter.encrypt(s) if encrypt else crypter.decrypt(s)

    return s


i = 1
len_argv = len(sys.argv)

if len_argv < 2:
    print(base_banner)
    sys.exit(0)

try:
    while i < len_argv:
        if sys.argv[i] in ('-h', '--help'):
            print(base_banner if sys.argv[i] == '-h' else full_banner)
            sys.exit(0)

        elif sys.argv[i] in ('-d', '--decrypt'):
            encrypt = False

        elif i < len_argv - 1 and sys.argv[i] in ('-a', '--alpha'):
            i += 1
            def_alpha = sys.argv[i]

        elif i < len_argv - 1 and sys.argv[i] in ('-c', '--chain'):
            i += 1
            chain = parse_chain(sys.argv[i])

        elif i < len_argv - 1 and sys.argv[i] in ('-o', '--output'):
            i += 1
            file_out = sys.argv[i]

        elif path.isfile(sys.argv[i]):
            file_in = sys.argv[i]

        elif file_in == sys.stdin:
            line += sys.argv[i]

        else:
            raise ValueError("invalid argument: '%s'\n" % sys.argv[i])

        i += 1
        len_argv = len(sys.argv)

except Exception as x:
    print("[!] %s" % str(x).capitalize())
    sys.exit(1)

try:
    if file_in != sys.stdin:
        file_in = open(file_in, "r")

    if file_out != sys.stdout:
        file_out = open(file_out, "w")

    if line:
        file_out.write(apply_chain(line, chain) + '\n')

        _close_io()
        sys.exit(0)

    for line in file_in:
        file_out.write(apply_chain(line.strip('\n'), chain) + '\n')

    _close_io()

except Exception as x:
    print("[!] %s" % str(x).capitalize())

    _close_io()
    sys.exit(2)
