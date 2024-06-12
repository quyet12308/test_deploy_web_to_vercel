import sqlite3


def init_db():
    conn = sqlite3.connect("tmp/users.db")
    cursor = conn.cursor()
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT NOT NULL
    )
    """
    )
    conn.commit()
    conn.close()


init_db()
