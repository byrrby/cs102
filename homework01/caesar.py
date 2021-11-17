import typing as tp


def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
    """
    Encrypts plaintext using a Caesar cipher.
    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    ciphertext = ""
    for letter in range(len(plaintext)):
        letter = plaintext[letter]
        if letter.isupper():
            ciphertext += chr((ord(letter) + shift - ord("A")) % 26 + ord("A"))
        elif letter.islower():
            ciphertext += chr((ord(letter) + shift - ord("a")) % 26 + ord("a"))
        else:
            ciphertext = ciphertext + letter
    return ciphertext


def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
    """
    Decrypts a ciphertext using a Caesar cipher.
    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    plaintext = ""
    for letter in range(len(ciphertext)):
        letter = ciphertext[letter]
        if letter.isupper():
            plaintext += chr((ord(letter) - shift - ord("A")) % 26 + ord("A"))
        elif letter.islower():
            plaintext += chr((ord(letter) - shift - ord("a")) % 26 + ord("a"))
        else:
            plaintext = plaintext + letter
    return plaintext


def caesar_breaker_brute_force(ciphertext: str, dictionary: tp.Set[str]) -> int:
    """
    Brute force breaking a Caesar cipher.
    """
    best_shift = 0
    return best_shift
