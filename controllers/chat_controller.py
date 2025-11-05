from models.db_model import Database
from models.super_encryption import super_encrypt, super_decrypt

class ChatController:
    def __init__(self):
        self.db = Database()

    def send_message(self, sender, receiver, content):
        enc_msg = super_encrypt(content, "securekey")
        sql = "INSERT INTO messages (sender, receiver, message) VALUES (%s, %s, %s)"
        self.db.execute(sql, (sender, receiver, enc_msg))

    def get_messages(self, user_a, user_b):
        sql = """
        SELECT sender, receiver, message FROM messages
        WHERE (sender=%s AND receiver=%s) OR (sender=%s AND receiver=%s)
        ORDER BY id ASC
        """
        rows = self.db.fetch(sql, (user_a, user_b, user_b, user_a))
        result = []
        for s, r, msg in rows:
            result.append((s, r, super_decrypt(msg, "securekey")))
        return result

    def get_all_users(self, exclude_username):
        sql = "SELECT username, last_active FROM users WHERE username != %s"
        return self.db.fetch(sql, (exclude_username,))
