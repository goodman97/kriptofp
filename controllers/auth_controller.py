from models.db_model import Database
from models.crypto_algorithms import hash_password
import datetime

class AuthController:
    def __init__(self):
        self.db = Database()

    def login_user(self, username, password):
        sql = "SELECT username, password FROM users WHERE username=%s"
        row = self.db.fetchone(sql, (username,))

        if not row:
            return False

        stored_username, stored_password = row

        hashed = hash_password(password)
        if stored_password == hashed:
            self.db.execute(
                "UPDATE users SET last_active=%s WHERE username=%s",
                (datetime.datetime.now(), username)
            )
            return True

        if stored_password == password:
            new_hashed = hash_password(password)
            try:
                self.db.execute(
                    "UPDATE users SET password=%s, last_active=%s WHERE username=%s",
                    (new_hashed, datetime.datetime.now(), username)
                )
                print(f"[INFO] Password for '{username}' rehashed and updated to new scheme.")
            except Exception as e:
                print(f"[WARN] Failed to update rehashed password for {username}: {e}")

            return True

        return False

    def register_user(self, username, password):
        sql = "SELECT username FROM users WHERE username=%s"
        exists = self.db.fetchone(sql, (username,))

        if exists:
            print(f"[WARN] Username '{username}' sudah digunakan.")
            return False

        hashed = hash_password(password)

        self.db.execute(
            "INSERT INTO users (username, password, last_active) VALUES (%s, %s, %s)",
            (username, hashed, datetime.datetime.now())
        )

        print(f"[INFO] User '{username}' berhasil diregister.")
        return True