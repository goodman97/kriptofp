from PIL import Image

class SteganoController:
    def __init__(self):

        self.terminator = "#####"

    def _to_bin(self, data):
        """Ubah string atau bytes menjadi representasi biner."""
        if isinstance(data, str):
            return ''.join(format(ord(i), '08b') for i in data)
        elif isinstance(data, (bytes, bytearray)):
            return ''.join(format(i, '08b') for i in data)
        else:
            raise TypeError("Data harus berupa string atau bytes")

    def embed_message(self, image_path, message, output_path):
        """
        Menyisipkan pesan ke dalam gambar (PNG) menggunakan metode LSB.
        Mengembalikan True jika berhasil, False jika gagal (misal pesan terlalu panjang).
        """
        try:
            image = Image.open(image_path)
            encoded = image.copy()
            width, height = image.size

            message_original_len = len(message)

            # DEBUG 1
            print("\n===== DEBUG EMBED =====")
            print(f"[+] Panjang pesan asli: {message_original_len} char")
            print(f"[+] Terminator: '{self.terminator}' (len={len(self.terminator)})")

            message += self.terminator
            binary_msg = self._to_bin(message)
            data_len = len(binary_msg)
            capacity = width * height * 3

            # DEBUG 2
            print(f"[+] Gambar: {width} x {height}")
            print(f"[+] Kapasitas gambar (bit): {capacity}")
            print(f"[+] Total bit pesan+terminator: {data_len}")

            if data_len > capacity:
                print(f"[ERROR] Pesan terlalu panjang ({data_len} bit > kapasitas {capacity} bit)")
                return False

            data_index = 0
            for y in range(height):
                for x in range(width):
                    pixel = list(image.getpixel((x, y)))
                    for n in range(3):
                        if data_index < data_len:
                            pixel[n] = pixel[n] & ~1 | int(binary_msg[data_index])
                            data_index += 1
                    encoded.putpixel((x, y), tuple(pixel))
                    if data_index >= data_len:
                        break
                if data_index >= data_len:
                    break

            print(f"[+] Embed selesai. Total bit tertanam: {data_index}")
            print("[+] STATUS: Embedded OK")
            print("=========================\n")

            encoded.save(output_path)
            return True

        except Exception as e:
            print(f"[ERROR] Gagal menyisipkan pesan: {e}")
            return False

    def extract_message(self, image_path):
        try:
            image = Image.open(image_path)

            bits = []
            decoded_chars = []
            terminator = self.terminator
            t_len = len(terminator)

            for value in (v & 1 for px in image.getdata() for v in px[:3]):
                bits.append(str(value))

                if len(bits) == 8:
                    byte = "".join(bits)
                    bits.clear()

                    try:
                        char = chr(int(byte, 2))
                    except:
                        char = "?"

                    decoded_chars.append(char)

                    # DEBUG PARTIAL PREVIEW
                    if len(decoded_chars) % 500 == 0:
                        print(f"[DEBUG] Sudah membaca {len(decoded_chars)} karakter...")

                    # Cek terminator
                    if len(decoded_chars) >= t_len:
                        if "".join(decoded_chars[-t_len:]) == terminator:
                            pesan_final = "".join(decoded_chars[:-t_len])
                            print("[+] Terminator ditemukan!")
                            print(f"[+] Panjang pesan diekstraksi: {len(pesan_final)} char")
                            print("============================\n")
                            return pesan_final

            print("[WARNING] Terminator tidak ditemukan.")
            print(f"[INFO] Total karakter terbaca: {len(decoded_chars)}")
            print("============================\n")
            return None

        except Exception as e:
            print(f"[ERROR] Ekstraksi gagal: {e}")
            return None