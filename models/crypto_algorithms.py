from hashlib import shake_128
from Crypto.Cipher import AES
import base64

# SHAKE-128 untuk password hashing
def hash_password(password):
    return shake_128(password.encode()).hexdigest(32)

# simulasi Camellia pakai AES untuk sementara
def camellia_encrypt(data, key):
    key = key.ljust(16, '0')[:16].encode()
    cipher = AES.new(key, AES.MODE_ECB)
    pad_len = 16 - len(data) % 16
    data += chr(pad_len) * pad_len
    enc = cipher.encrypt(data.encode())
    return base64.b64encode(enc).decode()

def camellia_decrypt(enc_data, key):
    key = key.ljust(16, '0')[:16].encode()
    cipher = AES.new(key, AES.MODE_ECB)
    dec = cipher.decrypt(base64.b64decode(enc_data)).decode()
    return dec[:-ord(dec[-1])]
