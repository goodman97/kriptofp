from hashlib import shake_128
import base64
from math import ceil
import struct


SBOX1 = [
    112,130,44,236,179,39,192,229,228,133,87,53,234,12,174,65,
    35,239,107,147,69,25,165,33,237,14,79,78,29,101,146,189,
    134,184,175,143,124,235,31,206,62,48,220,95,94,197,11,26,
    166,225,57,202,213,71,93,61,217,1,90,214,81,86,108,77,
    139,13,154,102,144,159,20,34,82,96,56,188,122,4,152,247,
    204,24,34,198,183,254,136,118,116,162,195,2,55,122,255,157,
    126,232,108,71,64,197,92,253,48,220,195,151,168,204,155,34,
    224,83,222,84,155,158,67,147,179,114,13,35,14,249,163,22,
    73,176,192,131,253,211,22,176,112,210,61,156,208,2,146,171,
    83,157,134,149,128,143,44,217,217,255,11,22,43,224,32,160
]


def camellia_f_function(block, subkey):
    x = block ^ subkey
    t1 = SBOX1[(x >> 56) & 0xFF]
    t2 = SBOX1[(x >> 48) & 0xFF]
    t3 = SBOX1[(x >> 40) & 0xFF]
    t4 = SBOX1[(x >> 32) & 0xFF]
    t5 = SBOX1[(x >> 24) & 0xFF]
    t6 = SBOX1[(x >> 16) & 0xFF]
    t7 = SBOX1[(x >> 8) & 0xFF]
    t8 = SBOX1[x & 0xFF]

    y = (
        (t1 << 56) | (t2 << 48) | (t3 << 40) |
        (t4 << 32) | (t5 << 24) | (t6 << 16) |
        (t7 << 8)  | t8
    )

    return y


def camellia_encrypt_block(key, block):
    left, right = struct.unpack(">QQ", block)
    k = struct.unpack(">QQQQ", key + b"\x00"* (32-len(key)))

    for i in range(3):
        left ^= camellia_f_function(right, k[i])
        left, right = right, left

    return struct.pack(">QQ", right, left)


def hash_password(password):
    return shake_128(password.encode()).hexdigest(64)


def pad(data):
    pad_len = 16 - (len(data) % 16)
    return data + chr(pad_len) * pad_len


def unpad(data):
    pad_len = ord(data[-1])
    return data[:-pad_len]


def camellia_encrypt(data, key):
    key = key.ljust(16, "0")[:16].encode()
    data = pad(data)

    out = b""
    for i in range(0, len(data), 16):
        block = data[i:i+16].encode()
        out += camellia_encrypt_block(key, block)

    return base64.b64encode(out).decode()


def camellia_decrypt(enc_data, key):
    key = key.ljust(16, "0")[:16].encode()
    raw = base64.b64decode(enc_data)

    out = b""
    for i in range(0, len(raw), 16):
        block = raw[i:i+16]
        out += camellia_encrypt_block(key, block) 

    return unpad(out.decode())
