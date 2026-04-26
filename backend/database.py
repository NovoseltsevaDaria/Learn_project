import sqlite3

DB_NAME = "hotel.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  # Чтобы результаты были как словари
    return conn

def init_db():
    """Создаёт таблицу rooms, если её нет"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS rooms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            room_number INTEGER NOT NULL UNIQUE,
            type TEXT NOT NULL,
            price_per_night REAL NOT NULL,
            is_available INTEGER NOT NULL,
            capacity INTEGER NOT NULL,
            description TEXT
        )
    """)
    conn.commit()
    conn.close()