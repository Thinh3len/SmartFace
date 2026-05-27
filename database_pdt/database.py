import sqlite3
import numpy as np
from datetime import datetime 

DB_PATH = "System.db"

def init_database():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    # 1. Bảng thông tin người dùng 
    cur.execute("""
        CREATE TABLE IF NOT EXISTS persons(
            id TEXT PRIMARY KEY, 
            name TEXT NOT NULL, 
            created_at TEXT DEFAULT (datetime('now', 'localtime'))
        )
    """)

    # 2. Bảng thông tin khuôn mặt (Đã đổi tên cột img_id thành face_embedding cho rõ nghĩa)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS person_id(
            person_id TEXT PRIMARY KEY, 
            face_embedding BLOB NOT NULL, 
            update_at TEXT DEFAULT (datetime('now', 'localtime')),
            created_at TEXT DEFAULT (datetime('now', 'localtime')),
            FOREIGN KEY(person_id) REFERENCES persons(id) ON DELETE CASCADE
        )
    """)
    conn.commit()
    conn.close()

# Thêm người dùng mới
def add_person(id, name):  # Đã bỏ dấu phẩy thừa ở (id, name,)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT OR IGNORE INTO persons(id, name)
            VALUES(?, ?)
        """, (id, name))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Lỗi khi thêm người dùng: {e}")
    finally:
        conn.close()

# Tìm kiếm thông tin người dùng
def get_person(id):  # Đã bỏ dấu phẩy thừa ở (id,)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("SELECT * FROM persons WHERE id = ?", (id,))
    row = cur.fetchone()
    
    # Khi SELECT dữ liệu thì KHÔNG cần conn.commit()
    conn.close()
    return row

# Kiểm tra người dùng tồn tại chưa
def person_exists(id):
    return get_person(id) is not None

# Lưu hoặc cập nhật khuôn mặt (Dưới dạng Vector Embedding)
def save_face(person_id, embedding_array):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    # Chuyển mảng NumPy sang dạng Bytes để lưu vào kiểu BLOB
    embedding_bytes = embedding_array
    
    cur.execute("""
        INSERT OR REPLACE INTO person_id(person_id, face_embedding)
        VALUES(?, ?)
    """, (person_id, embedding_bytes))
    conn.commit()
    conn.close()

# Hàm bổ sung: Lấy khuôn mặt ra và chuyển ngược lại thành mảng NumPy khi cần nhận diện
def get_face(person_id, dtype=np.float32):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    cur.execute("SELECT face_embedding FROM person_id WHERE person_id = ?", (person_id,))
    row = cur.fetchone()
    conn.close()
    
    if row:
        # Chuyển từ định dạng Bytes ngược về mảng NumPy
        return np.frombuffer(row[0], dtype=dtype)
    return None