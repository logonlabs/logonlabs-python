# AES 256 encryption/decryption using pycrypto library
 
import base64
from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Protocol.KDF import PBKDF2
 
BLOCK_SIZE = 16
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
unpad = lambda s: s[:-ord(s[len(s) - 1:])]

iterations = 1000
dkLen = 32
 
def encrypt(message, password):
    salt = Random.get_random_bytes(dkLen)
    kdf = PBKDF2(password, salt, dkLen, iterations)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(kdf, AES.MODE_CBC, iv)
    message = pad(message)
    return base64.b64encode(salt + iv + cipher.encrypt(message))


def decrypt(enc, password):
    enc = base64.b64decode(enc)
    salt = enc[:dkLen]
    kdf = PBKDF2(password, salt, dkLen, iterations)
    iv = enc[dkLen:(dkLen + 16)]
    cipher = AES.new(kdf, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(enc[dkLen + 16:]))
