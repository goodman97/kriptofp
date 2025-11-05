def vigenere_encrypt(text, key):
    key = key.lower()
    result = ""
    for i, char in enumerate(text):
        if char.isalpha():
            base = 'A' if char.isupper() else 'a'
            shift = ord(key[i % len(key)]) - ord('a')
            result += chr((ord(char) - ord(base) + shift) % 26 + ord(base))
        else:
            result += char
    return result

def vigenere_decrypt(text, key):
    key = key.lower()
    result = ""
    for i, char in enumerate(text):
        if char.isalpha():
            base = 'A' if char.isupper() else 'a'
            shift = ord(key[i % len(key)]) - ord('a')
            result += chr((ord(char) - ord(base) - shift) % 26 + ord(base))
        else:
            result += char
    return result

def block_permute(text, block_size=4):
    blocks = [text[i:i+block_size] for i in range(0, len(text), block_size)]
    return ''.join(block[::-1] for block in blocks)

def super_encrypt(text, key):
    return block_permute(vigenere_encrypt(text, key))

def super_decrypt(text, key):
    return vigenere_decrypt(block_permute(text), key)
