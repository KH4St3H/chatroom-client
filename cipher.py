import hashlib

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad


class AESCipher:
    def __init__(self, key):
        self.key = self.hash_password(key)

    def encrypt(self, data):
        iv = get_random_bytes(AES.block_size)

        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return iv + cipher.encrypt(pad(data, AES.block_size))

    def decrypt(self, raw):
        cipher = AES.new(self.key, AES.MODE_CBC, raw[:AES.block_size])
        # print(b64encode(cipher.decrypt(raw[AES.block_size:])))

        return unpad(cipher.decrypt(raw[AES.block_size:]), AES.block_size)

    def hash_password(self, password):
        hash = hashlib.sha1()
        hash.update(password)

        return hash.digest()[:16]
