from models.db_model import Database
from models.crypto_algorithms import hash_password
import datetime

class AuthController:
    def __init__(self):
        self.db = Database()

    def login_user(self, username, password):
        hashed = hash_password(password)
        sql = "SELECT * FROM users WHERE username=%s AND password=%s"
        result = self.db.fetch(sql, (username, hashed))

        if result:
            self.db.execute(
                "UPDATE users SET last_active=%s WHERE username=%s",
                (datetime.datetime.now(), username)
            )
            return True
        else:
            self.db.execute(
                "INSERT INTO users (username, password, last_active) VALUES (%s, %s, %s)",
                (username, hashed, datetime.datetime.now())
            )
            print(f"[INFO] User baru '{username}' ditambahkan ke database.")
            return True
