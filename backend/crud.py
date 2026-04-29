from database import get_connection

def get_all_rooms():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM rooms").fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_room_by_id(room_id: int):
    conn = get_connection()
    row = conn.execute("SELECT * FROM rooms WHERE id = ?", (room_id,)).fetchone()
    conn.close()
    return dict(row) if row else None

def create_room(room_data: dict):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO rooms (room_number, type, price_per_night, is_available, capacity, description, has_washing_machine, has_dishwasher)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        room_data["room_number"],
        room_data["type"],
        room_data["price_per_night"],
        int(room_data["is_available"]),
        room_data["capacity"],
        room_data.get("description"),
        int(room_data.get("has_washing_machine", False)),
        int(room_data.get("has_dishwasher", False))
    ))
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return new_id

def update_room(room_id: int, room_data: dict):
    conn = get_connection()
    conn.execute("""
        UPDATE rooms 
        SET room_number = ?, type = ?, price_per_night = ?, is_available = ?, capacity = ?, description = ?, has_washing_machine = ?, has_dishwasher = ?
        WHERE id = ?
    """, (
        room_data["room_number"],
        room_data["type"],
        room_data["price_per_night"],
        int(room_data["is_available"]),
        room_data["capacity"],
        room_data.get("description"),
        int(room_data.get("has_washing_machine", False)),
        int(room_data.get("has_dishwasher", False)),
        room_id
    ))
    conn.commit()
    conn.close()

def delete_room(room_id: int):
    conn = get_connection()
    conn.execute("DELETE FROM rooms WHERE id = ?", (room_id,))
    conn.commit()
    conn.close()