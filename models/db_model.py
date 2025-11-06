import mysql.connector
from mysql.connector import Error
from config.db_config import DB_CONFIG

class Database:
    def __init__(self):
        try:
            self.conn = mysql.connector.connect(**DB_CONFIG, autocommit=True)
            self.cursor = self.conn.cursor()
        except Error as e:
            print(f"[DB ERROR] {e}")

    def fetch(self, sql, params=None):
        self.cursor.execute(sql, params or ())
        return self.cursor.fetchall()

    def execute(self, sql, params=None):
        self.cursor.execute(sql, params or ())
        self.conn.commit()

    def close(self):
        self.cursor.close()
        self.conn.close()
