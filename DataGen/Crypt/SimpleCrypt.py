import base64
from itertools import cycle


def encrypt(message, key):
    cipher = (''.join(chr(ord(x) ^ y) for x, y in zip(message, cycle(key))))
    cipher = cipher.encode("utf-8")
    # cipher = base64.b64encode(cipher)

    return cipher


def decrypt(cipher, key):
    # cipher = base64.b64decode(cipher)
    cipher = cipher.decode('utf-8')
    message = ''.join(chr(ord(x) ^ y) for x, y in zip(cipher, cycle(key)))

    return message
