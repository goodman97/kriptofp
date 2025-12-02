import os
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend


class FileController:
    def __init__(self, key="seedsecurekey1234"):
        self.key = key.ljust(16, '0')[:16].encode()

    def pad(self, data: bytes) -> bytes:
        pad_len = 16 - (len(data) % 16)
        return data + bytes([pad_len]) * pad_len

    def unpad(self, data: bytes) -> bytes:
        pad_len = data[-1]
        if pad_len < 1 or pad_len > 16:
            raise ValueError("Invalid padding")
        return data[:-pad_len]

    def encrypt_file(self, input_path: str) -> str:
        iv = os.urandom(16)
        cipher = Cipher(
            algorithms.SEED(self.key),
            modes.CBC(iv),
            backend=default_backend()
        )
        encryptor = cipher.encryptor()

        with open(input_path, "rb") as f:
            data = f.read()

        enc_data = encryptor.update(self.pad(data)) + encryptor.finalize()

        return base64.b64encode(iv + enc_data).decode("utf-8")

    def decrypt_file(self, enc_base64: str) -> bytes:
        raw = base64.b64decode(enc_base64)

        if len(raw) < 16:
            raise ValueError("Data terenkripsi corrupt (IV hilang).")

        iv = raw[:16]
        ciphertext = raw[16:]

        cipher = Cipher(
            algorithms.SEED(self.key),
            modes.CBC(iv),
            backend=default_backend()
        )
        decryptor = cipher.decryptor()

        decrypted = decryptor.update(ciphertext) + decryptor.finalize()

        return self.unpad(decrypted)