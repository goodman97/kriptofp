from models.db_model import Database
from models.super_encryption import super_encrypt, super_decrypt
from controllers.file_controller import FileController

class ChatController:
    def __init__(self):
        self.db = Database()
        self.file_ctrl = FileController()

    def send_message(self, sender, receiver, message, msg_type="text", filename=None):
        if msg_type == "text":
            encrypted = super_encrypt(message, "securekey")
        else:
            encrypted = message  # file → message = filename

        self.db.execute(
            "INSERT INTO messages (sender, receiver, message, msg_type, filename) VALUES (%s, %s, %s, %s, %s)",
            (sender, receiver, encrypted, msg_type, filename)
        )

    def get_all_users(self, exclude_username):
        """
        Kembalikan list tuple (username, last_active) untuk semua user selain exclude_username.
        Dipakai oleh ChatWindow.load_user_list().
        """
        sql = "SELECT username, last_active FROM users WHERE username != %s"
        return self.db.fetch(sql, (exclude_username,))

    # FILE dikirim lewat folder, bukan lewat DB
    def send_file(self, sender, receiver, filename):
        sql = """
        INSERT INTO messages (sender, receiver, message, msg_type, filename)
        VALUES (%s, %s, %s, %s, %s)
        """
        # message di DB dikosongkan
        self.db.execute(sql, (sender, receiver, "", "file", filename))

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
                try:
                    decrypted = super_decrypt(msg, "securekey")   # ⬅ Dekripsi di sini!
                except:
                    decrypted = "[DECRYPTION ERROR]"

                result.append((s, r, decrypted, msg_type, None))

            else:
                # file & stego -> message kosong, hanya filename
                result.append((s, r, "", msg_type, filename))

        return result