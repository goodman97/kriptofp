from PIL import Image

class SteganoController:
    def __init__(self):
        self.terminator = "#####"

    def _to_bin(self, data):
        """Convert string or bytes to binary string."""
        if isinstance(data, str):
            return ''.join(format(ord(i), '08b') for i in data)
        elif isinstance(data, (bytes, bytearray)):
            return ''.join(format(i, '08b') for i in data)
        else:
            raise TypeError("Data must be string or bytes")

    def embed_message(self, image_path, message, output_path):
        """Embed a secret message into an image. Returns True if successful."""
        image = Image.open(image_path)
        encoded = image.copy()
        width, height = image.size

        message += self.terminator
        binary_msg = self._to_bin(message)
        data_len = len(binary_msg)

        # cek kapasitas gambar
        if data_len > width * height * 3:
            print("Error: Message too long to encode in this image.")
            return False

        data_index = 0
        for y in range(height):
            for x in range(width):
                pixel = list(image.getpixel((x, y)))
                for n in range(3):  # RGB channels
                    if data_index < data_len:
                        pixel[n] = pixel[n] & ~1 | int(binary_msg[data_index])
                        data_index += 1
                encoded.putpixel((x, y), tuple(pixel))
                if data_index >= data_len:
                    encoded.save(output_path)
                    return True
        return False

    def extract_message(self, image_path):
        """Extract hidden message from an image."""
        image = Image.open(image_path)
        binary_data = ""
        for pixel in list(image.getdata()):
            for value in pixel[:3]:  # RGB channels
                binary_data += str(value & 1)

        all_bytes = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]
        decoded_data = ""
        for byte in all_bytes:
            decoded_data += chr(int(byte, 2))
            if decoded_data.endswith(self.terminator):
                break
        return decoded_data[:-len(self.terminator)]
