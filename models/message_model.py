import sqlite3
from config.db_config import DB_PATH

class Message:
    def __init__(self, sender, receiver, content, msg_type="text", filename=None):
        self.sender = sender
        self.receiver = receiver
        self.content = content
        self.msg_type = msg_type
        self.filename = filename


class MessageModel:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sender TEXT,
                receiver TEXT,
                msg_type TEXT,
                filename TEXT,
                content TEXT
            )
        """)
        self.conn.commit()

    def save_message(self, message: Message):
        """Simpan objek Message ke database"""
        self.cursor.execute("""
            INSERT INTO messages (sender, receiver, msg_type, filename, content)
            VALUES (?, ?, ?, ?, ?)
        """, (message.sender, message.receiver, message.msg_type, message.filename, message.content))
        self.conn.commit()

    def get_all_messages(self):
        """Ambil semua pesan dari DB sebagai list of Message"""
        self.cursor.execute("""
            SELECT sender, receiver, content, msg_type, filename
            FROM messages ORDER BY id ASC
        """)
        rows = self.cursor.fetchall()
        messages = [
            Message(sender=row[0], receiver=row[1], content=row[2], msg_type=row[3], filename=row[4])
            for row in rows
        ]
        return messages

    def close(self):
        self.conn.close()
