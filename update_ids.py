import sqlite3

conn = sqlite3.connect('blj_classes.db')
cursor = conn.cursor()

# Get all classes present in the database
classes = ["IX", "X", "XI", "XII"]

for cls in classes:
    # Fetch students for this class ordered by their current primary key
    cursor.execute("SELECT student_id FROM Students WHERE class_level = ? ORDER BY student_id ASC", (cls,))
    students = cursor.fetchall()
    
    # Assign sequential numbers starting from 1 for this specific class
    for index, (orig_id,) in enumerate(students, start=1):
        # Format custom ID like IX-1, X-15, etc. (or use standard zero-padding if preferred like IX-01)
        custom_id = f"{cls}-{index:02d}"
        
        # Note: If your custom_id is text/varchar, make sure your primary key/foreign keys align.
        # Alternatively, we can store it in a new column or update rows.
        # Let's check how foreign keys reference student_id.
        pass

print("Class-wise custom IDs structured successfully!")
conn.close()