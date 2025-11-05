import os
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

class FileController:
    def __init__(self, key="seedsecurekey1234"):
        # SEED key harus 16 byte (128 bit)
        self.key = key.ljust(16, '0')[:16].encode()

    # Padding PKCS#7
    def pad(self, data):
        pad_len = 16 - (len(data) % 16)
        return data + bytes([pad_len]) * pad_len

    def unpad(self, data):
        pad_len = data[-1]
        return data[:-pad_len]

    # Enkripsi file
    def encrypt_file(self, input_path):
        iv = os.urandom(16)
        cipher = Cipher(algorithms.SEED(self.key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()

        with open(input_path, "rb") as f:
            data = f.read()
        enc_data = encryptor.update(self.pad(data)) + encryptor.finalize()

        return base64.b64encode(iv + enc_data).decode("utf-8")

    # Dekripsi file
    def decrypt_file(self, enc_base64):
        raw = base64.b64decode(enc_base64)
        iv = raw[:16]
        ciphertext = raw[16:]

        cipher = Cipher(algorithms.SEED(self.key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        dec_data = self.unpad(decryptor.update(ciphertext) + decryptor.finalize())

        return dec_data