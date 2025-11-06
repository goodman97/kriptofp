from models.db_model import Database
from models.super_encryption import super_encrypt, super_decrypt
from controllers.file_controller import FileController


class ChatController:
    def __init__(self):
        self.db = Database()
        self.file_ctrl = FileController()

    def send_message(self, sender, receiver, content, msg_type="text", filename=None):
        enc_msg = super_encrypt(content, "securekey")
        sql = """
            INSERT INTO messages (sender, receiver, message, msg_type, filename)
            VALUES (%s, %s, %s, %s, %s)
        """
        self.db.execute(sql, (sender, receiver, enc_msg, msg_type, filename))


    def send_file(self, sender, receiver, filepath):
        encrypted_base64 = self.file_ctrl.encrypt_file(filepath)
        filename = filepath.split("/")[-1]
        sql = """
        INSERT INTO messages (sender, receiver, message, msg_type, filename)
        VALUES (%s, %s, %s, %s, %s)
        """
        self.db.execute(sql, (sender, receiver, encrypted_base64, "file", filename))

    
    def send_stego_image(self, sender, receiver, image_filename):
        sql = """
        INSERT INTO messages (sender, receiver, message, msg_type, filename)
        VALUES (%s, %s, %s, %s, %s)
        """
        self.db.execute(sql, (sender, receiver, "", "stegano", image_filename))


    def get_messages(self, user_a, user_b):
        sql = """
        SELECT sender, receiver, message, msg_type, filename
        FROM messages
        WHERE (sender=%s AND receiver=%s) OR (sender=%s AND receiver=%s)
        ORDER BY id ASC
        """
        rows = self.db.fetch(sql, (user_a, user_b, user_b, user_a))
        result = []

        for s, r, msg, msg_type, filename in rows:
            if msg_type == "text":
                decrypted = super_decrypt(msg, "securekey")
                result.append((s, r, decrypted, msg_type, None))
            elif msg_type == "file":
                result.append((s, r, msg, msg_type, filename))
            elif msg_type == "stegano":
                # Pesan steganografi: tampilkan gambar yang dikirim
                result.append((s, r, msg, msg_type, filename))
        
        if rows:
            self.last_message_id = rows[-1][0] if hasattr(self, 'last_message_id') else None

        return result


    def decrypt_file_from_db(self, enc_base64, output_path):
        decrypted_bytes = self.file_ctrl.decrypt_file(enc_base64)
        with open(output_path, "wb") as f:
            f.write(decrypted_bytes)
        return output_path

    def get_all_users(self, exclude_username):
        sql = "SELECT username, last_active FROM users WHERE username != %s"
        return self.db.fetch(sql, (exclude_username,))