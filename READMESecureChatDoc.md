# 🔐 Secure Chat – Multi-Layered Cryptography & Steganography System

Dokumentasi ini menjelaskan penggunaan dan peran dari setiap algoritma yang digunakan dalam proyek **Secure Chat berbasis kriptografi dan steganografi**.

---

## 🧩 Arsitektur Sistem

Aplikasi Secure Chat ini memiliki **beberapa lapisan keamanan** yang saling bekerja sama:

1. **Hashing (SHAKE128)** – mengubah password menjadi kunci aman.
2. **Enkripsi Pesan (Camellia / Super Encryption / SEED-CBC)** – melindungi isi pesan.
3. **Steganografi (Enhanced LSB)** – menyembunyikan pesan terenkripsi ke dalam gambar.
4. **Transmisi** – mengirimkan gambar hasil steganografi ke penerima.

---

## 1️⃣ SHAKE128 – Hashing Dinamis

### 📘 Fungsi
SHAKE128 digunakan untuk **menghasilkan kunci enkripsi dari password pengguna**.  
Karena SHAKE128 bersifat **extendable output**, kita bisa menentukan panjang hash yang diinginkan (misalnya 16 byte untuk kunci Camellia/SEED).

### 💻 Implementasi
```python
from hashlib import shake_128

def hash_password(password):
    return shake_128(password.encode()).hexdigest(64)
```

### 🧠 Peran
- Mengubah password user menjadi key unik.
- Mencegah penyimpanan password dalam bentuk plaintext.
- Memberi entropi tinggi untuk algoritma enkripsi selanjutnya.

---

## 2️⃣ Camellia Cipher – Enkripsi Blok Simetris

### 📘 Fungsi
Camellia digunakan untuk **mengenkripsi data teks sebelum disisipkan ke gambar**.  
Algoritma ini mirip dengan AES, memiliki **128-bit blok**, dan aman secara kriptografis.

### 💻 Implementasi
```python
from Cryptodome.Cipher import Camellia
import base64

def camellia_encrypt(data, key):
    key = key.ljust(16, '0')[:16].encode()
    cipher = Camellia.new(key, Camellia.MODE_ECB)
    pad_len = 16 - len(data) % 16
    data += chr(pad_len) * pad_len
    enc = cipher.encrypt(data.encode())
    return base64.b64encode(enc).decode()

def camellia_decrypt(enc_data, key):
    key = key.ljust(16, '0')[:16].encode()
    cipher = Camellia.new(key, Camellia.MODE_ECB)
    dec = cipher.decrypt(base64.b64decode(enc_data)).decode()
    return dec[:-ord(dec[-1])]
```

### 🧠 Peran
- Melindungi isi pesan sebelum proses embedding (penyisipan).
- Menambah keamanan terhadap serangan plaintext langsung.
- Memberi lapisan enkripsi cepat dan ringan untuk pesan teks.

---

## 3️⃣ Super Encryption – Kombinasi Vigenère + Block Permutation

### 📘 Fungsi
Super Encryption digunakan untuk **meningkatkan kekuatan enkripsi teks** dengan menggabungkan dua teknik:
1. **Vigenère Cipher** → menggeser huruf berdasarkan kunci.
2. **Block Permutation** → membalik urutan setiap blok karakter.

### 💻 Implementasi
```python
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

def block_permute(text, block_size=4):
    blocks = [text[i:i+block_size] for i in range(0, len(text), block_size)]
    return ''.join(block[::-1] for block in blocks)

def super_encrypt(text, key):
    return block_permute(vigenere_encrypt(text, key))
```

### 🧠 Peran
- Menyediakan **lapisan enkripsi tambahan** sebelum embedding.  
- Menyulitkan analisis pola ciphertext (frekuensi huruf).  
- Aman untuk pesan teks pendek dan ringan secara komputasi.

---

## 4️⃣ SEED-CBC – Enkripsi Berantai Aman

### 📘 Fungsi
Algoritma SEED (dikembangkan oleh KISA, Korea) digunakan dalam mode **CBC (Cipher Block Chaining)** untuk mengenkripsi data dengan tingkat keamanan tinggi.  
Setiap blok bergantung pada blok sebelumnya, sehingga pola data tidak mudah ditebak.

### 💻 Implementasi (dengan AES sebagai analogi)
```python
from Cryptodome.Cipher import AES
from Crypto.Util.Padding import pad, unpad

def seed_encrypt(plaintext, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(plaintext.encode(), 16))
    return ciphertext

def seed_decrypt(ciphertext, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = unpad(cipher.decrypt(ciphertext), 16)
    return decrypted.decode()
```

### 🧠 Peran
- Menyediakan lapisan enkripsi blok yang lebih kuat.  
- Menjamin keamanan tinggi jika digunakan bersama SHAKE128 sebagai pembangkit kunci.  
- Mencegah pola berulang pada ciphertext.

---

## 5️⃣ Enhanced LSB – Steganografi pada Gambar

### 📘 Fungsi
Enhanced LSB digunakan untuk **menyembunyikan pesan terenkripsi ke dalam gambar PNG**.  
Metode ini mengganti **bit paling tidak signifikan (Least Significant Bit)** dari setiap channel warna RGB.

### 💻 Implementasi
```python
from PIL import Image

def embed_message(image_path, message, output_path):
    image = Image.open(image_path)
    encoded = image.copy()
    width, height = image.size
    message += "#####"
    binary_msg = ''.join(format(ord(c), '08b') for c in message)
    data_index = 0
    for y in range(height):
        for x in range(width):
            pixel = list(image.getpixel((x, y)))
            for n in range(3):
                if data_index < len(binary_msg):
                    pixel[n] = pixel[n] & ~1 | int(binary_msg[data_index])
                    data_index += 1
            encoded.putpixel((x, y), tuple(pixel))
            if data_index >= len(binary_msg):
                break
        if data_index >= len(binary_msg):
            break
    encoded.save(output_path)
```

### 🧠 Peran
- Menyembunyikan ciphertext agar tidak terlihat oleh mata manusia.
- Mengubah hanya bit terakhir tiap channel RGB (perubahan visual minimal).  
- Menggunakan terminator `"#####"` untuk menandai akhir pesan.

---

## 🔗 Alur Lengkap Sistem

```text
[User Input Pesan + Password]
          │
          ▼
[Hash Password → SHAKE128]
          │
          ▼
[Enkripsi Pesan → Camellia / Super Encrypt / SEED-CBC]
          │
          ▼
[Embed Ciphertext → Enhanced LSB]
          │
          ▼
[Gambar Stego Tersimpan & Dikirim]
          │
          ▼
[Penerima Ekstrak Pesan → LSB Extract]
          │
          ▼
[Dekripsi Pesan → Camellia / Super Decrypt / SEED-CBC]
          │
          ▼
[Pesan Asli Ditampilkan]
```

---

## 🧠 Kesimpulan

| Lapisan | Algoritma | Tujuan Utama | Jenis |
|----------|------------|---------------|--------|
| 1 | SHAKE128 | Hash password untuk menghasilkan key | Hashing |
| 2 | Camellia | Enkripsi pesan teks cepat | Block Cipher |
| 3 | Super Encryption | Lapisan enkripsi tambahan (Vigenère + blok) | Stream + Permutation |
| 4 | SEED-CBC | Enkripsi chaining simetris | Block Cipher |
| 5 | Enhanced LSB | Menyembunyikan ciphertext di gambar | Steganografi |

🔒 Kombinasi algoritma ini membentuk sistem **multi-layer security**, di mana:
- Hashing → melindungi kunci  
- Enkripsi → melindungi isi pesan  
- Steganografi → melindungi eksistensi pesan

---

📄 *Dokumentasi ini dibuat untuk mendukung implementasi proyek Secure Chat berbasis Kriptografi dan Steganografi.*
