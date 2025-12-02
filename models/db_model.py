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
            self.conn = None
            self.cursor = None

    def fetch(self, sql, params=None):
        """Return all rows as list of tuples."""
        if not self.cursor:
            return []
        self.cursor.execute(sql, params or ())
        return self.cursor.fetchall()

    def fetchone(self, sql, params=None):
        """Return single row as tuple or None."""
        if not self.cursor:
            return None
        self.cursor.execute(sql, params or ())
        return self.cursor.fetchone()

    def execute(self, sql, params=None):
        if not self.cursor:
            raise RuntimeError("Database connection is not available.")
        self.cursor.execute(sql, params or ())
        self.conn.commit()

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()