from math import gcd as _bltn_gcd

_def_leet  = '48cd3f9h1jklmn0pqr57uvwxy2'

_morse_code = (
    ('a', '.-'),    ('b', '-...'),  ('c', '-.-.'),  ('d', '-..'),   ('e', '.'),
    ('f', '..-.'),  ('g', '--.'),   ('h', '....'),  ('i', '..'),    ('j', '.---'),
    ('k', '-.-'),   ('l', '.-..'),  ('m', '--'),    ('n', '-.'),    ('o', '---'),
    ('p', '.--.'),  ('q', '--.-'),  ('r', '.-.'),   ('s', '...'),   ('t', '-'),
    ('u', '..-'),   ('v', '...-'),  ('w', '.--'),   ('x', '-..-'),  ('y', '-.--'),
    ('z', '--..'),  ('0', '-----'), ('1', '.----'), ('2', '..---'), ('3', '...--'),
    ('4', '....-'), ('5', '.....'), ('6', '-....'), ('7', '--...'), ('8', '---..'),
    ('9', '----.'), (' ', '/')
)

## Ciphers ##
# Generic class
class Cipher(object):
    _key   = None
    _alpha = None

    encrypt = lambda self, s: self._crypt(list(s))
    decrypt = lambda self, s: self._crypt(list(s), encrypt = False)


class Affine(Cipher):
    def __init__(self, key_x, key_y, alpha):
        len_alpha = len(alpha)

        if _bltn_gcd(key_x, len_alpha) != 1:
            raise ValueError(
                "The first value and %i must be relatively prime" % len_alpha
            )

        self._key = (key_x, key_y)
        self._alpha = alpha.lower()


    def _crypt(self, s, encrypt = True):
        x, y = self._key

        m_inverse_x = 0
        len_alpha = len(self._alpha)

        # Find the multiplicative inverse of x
        for i in range(len_alpha):
            if (x * i) % len_alpha == 1:
                m_inverse_x = i

        for i in range(len(s)):
            alpha = self._alpha.upper() if s[i].isupper() else self._alpha

            if s[i] in alpha:
                index = alpha.index(s[i])
                op = (x * index + y) if encrypt else (m_inverse_x * (index - y))

                s[i] = alpha[op % len_alpha]

        return ''.join(s)


class Atbash(Cipher):
    def __init__(self, alpha):
        self._alpha = alpha.lower()


    def _crypt(self, s, encrypt = True):
        for i in range(len(s)):
            alpha = self._alpha.upper() if s[i].isupper() else self._alpha

            if s[i] in alpha:
                s[i] = alpha[-alpha.index(s[i]) - 1]

        return ''.join(s)


class Beaufort(Cipher):
    def __init__(self, key, alpha):
        if not type(key) == str:
            raise TypeError(
                "class '%s' where 'str' was expected" % type(key).__name__
            )

        if any([c not in alpha.lower() for c in key.lower()]):
            raise ValueError("valid key characters are '%s'" % alpha)

        self._key   = key.lower()
        self._alpha = alpha.lower()


    def _crypt(self, s, encrypt = True):
        key_i = -1

        len_key   = len(self._key)
        len_alpha = len(self._alpha)

        for i in range(len(s)):
            if s[i].lower() not in self._alpha:
                continue

            key_i += 1
            key   = self._key.upper()   if s[i].isupper() else self._key
            alpha = self._alpha.upper() if s[i].isupper() else self._alpha

            alpha_i     = alpha.index(s[i])
            key_alpha_i = alpha.index(key[key_i % len_key])

            for j in range(0, len_alpha):
                if alpha[(alpha_i + j) % len_alpha] == alpha[key_alpha_i]:
                    s[i] = alpha[j]
                    break

        return ''.join(s)


class Caesar(Cipher):
    def __init__(self, key, alpha):
        if key < 1:
            raise ValueError("Invalid shift value")

        self._key   = key
        self._alpha = alpha


    def _crypt(self, s, encrypt = True):
        len_alpha = len(self._alpha)
        shift = (self._key % len_alpha) if encrypt else -(self._key % len_alpha)

        for i in range(len(s)):
            alpha = self._alpha.upper() if s[i].isupper() else self._alpha

            if s[i] in alpha:
                s[i] = alpha[(alpha.index(s[i]) + shift) % 26]

        return ''.join(s)


class SimpleSubstitution(Cipher):
    def __init__(self, key, alpha):
        if not type(key) == str:
            raise TypeError(
                "class '%s' where 'str' was expected" % type(key).__name__
            )

        if len(set(key)) != len(alpha):
            raise ValueError(
                "The key must contain %i unique characters" % len(alpha)
            )

        self._key   = key
        self._alpha = alpha


    def _crypt(self, s, encrypt = True):
        d = {k:v for k, v in (zip(self._alpha, self._key)
             if encrypt else  zip(self._key, self._alpha))}

        return ''.join(d[s[i]] if s[i] in d else s[i] for i in range(len(s)))


class Vigenere(Cipher):
    def __init__(self, key, alpha):
        if not type(key) == str:
            raise TypeError(
                "class '%s' where 'str' was expected" % type(key).__name__
            )

        if any([c not in alpha.lower() for c in key.lower()]):
            raise ValueError(
                "valid key characters are '%s'" % alpha
            )

        self._key   = key.lower()
        self._alpha = alpha.lower()


    def _crypt(self, s, encrypt = True):
        key_i = -1

        len_key   = len(self._key)
        len_alpha = len(self._alpha)

        for i in range(len(s)):
            if s[i].lower() not in self._alpha:
                continue

            key_i += 1
            key    = self._key.upper()   if s[i].isupper() else self._key
            alpha  = self._alpha.upper() if s[i].isupper() else self._alpha

            key_alpha_i = alpha.index(key[key_i % len_key])
            shift = key_alpha_i if encrypt else -key_alpha_i

            s[i] = alpha[(alpha.index(s[i]) + shift) % len_alpha]


        return ''.join(s)


## Encodings ##
def leet(s, alpha, encrypt = True):
    crypter = SimpleSubstitution(_def_leet, alpha)
    return crypter.encrypt(s) if encrypt else crypter.decrypt(s)


def morse(s, encrypt = True):
    if encrypt:
        joint = ' '
        d = {f1:f2 for f1, f2 in _morse_code}

    else:
        joint = ''

        s = [ss.strip() for ss in s.split()]
        d = {f2:f1 for f1, f2 in _morse_code}

    return joint.join([d.get(c.lower()) if c.lower() in d else c for c in s])


def frequency_as_index(s, alpha, encrypt = True):
    len_alpha = len(alpha)

    if encrypt:
        joint = ' / '
        s = s.split()
        gen_char = lambda c: '.' * (alpha.index(c) + 1) if c in alpha else c

        for i in range(len(s)):
            s[i] = ' '.join([gen_char(c) for c in s[i].lower()])
    else:
        joint = ' '
        s = s.split('/')
        gen_char = lambda ss: alpha[(len(ss) - 1) % len_alpha]

        for i in range(len(s)):
            s[i] = ''.join([gen_char(ss) for ss in s[i].lower().split()])

    return joint.join(s)


## String manipulation ##
toggle = lambda s: ''.join(c.lower() if c.isupper() else c.upper() for c in s)
