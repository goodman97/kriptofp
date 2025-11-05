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

            message += self.terminator
            binary_msg = self._to_bin(message)
            data_len = len(binary_msg)
            capacity = width * height * 3

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

            encoded.save(output_path)
            return True

        except Exception as e:
            print(f"[ERROR] Gagal menyisipkan pesan: {e}")
            return False

    def extract_message(self, image_path):
        """
        Mengekstrak pesan tersembunyi dari gambar stego.
        Mengembalikan string pesan asli tanpa terminator.
        """
        try:
            image = Image.open(image_path)
            binary_data = ""
            for pixel in list(image.getdata()):
                for value in pixel[:3]:
                    binary_data += str(value & 1)

            all_bytes = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]
            decoded_data = ""
            for byte in all_bytes:
                decoded_data += chr(int(byte, 2))
                if decoded_data.endswith(self.terminator):
                    break

            if not decoded_data.endswith(self.terminator):
                print("[WARNING] Tidak ditemukan pesan tersembunyi dalam gambar.")
                return None

            return decoded_data[:-len(self.terminator)]

        except Exception as e:
            print(f"[ERROR] Gagal mengekstrak pesan: {e}")
            return None