import sqlite3
import hashlib

conn = sqlite3.connect('blj_classes.db')
cursor = conn.cursor()

# Create Teachers table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Teachers (
        teacher_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL
    )
''')

# Insert a default admin/teacher account (Username: sir, Password: blj123)
default_user = "sir"
default_pass_hash = hashlib.sha256("blj123".encode()).hexdigest()

cursor.execute('''
    INSERT OR IGNORE INTO Teachers (username, password_hash) 
    VALUES (?, ?)
''', (default_user, default_pass_hash))

conn.commit()
conn.close()
print("Teacher authentication table created and default login added!")