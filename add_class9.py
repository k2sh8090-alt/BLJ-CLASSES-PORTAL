import sqlite3

# Connect to your database
conn = sqlite3.connect('blj_classes.db')
cursor = conn.cursor()

# List of Class IX students
students = [
    ('Tanav', 'Sharma', 'IX', 'A', 'Pending', '0000000000'),
    ('Nevin', '', 'IX', 'A', 'Pending', '0000000000'),
    ('Ronav', 'Moolwani', 'IX', 'A', 'Pending', '0000000000'),
    ('Hridyansh', 'Gupta', 'IX', 'A', 'Pending', '0000000000'),
    ('Sourish', 'Gupta', 'IX', 'A', 'Pending', '0000000000'),
    ('Parinidhi', 'Agarwal', 'IX', 'A', 'Pending', '0000000000'),
    ('Akshita', 'Sethi', 'IX', 'A', 'Pending', '0000000000'),
    ('Tejasvi', 'Gehlot', 'IX', 'A', 'Pending', '0000000000'),
    ('Jinal', 'Jangid', 'IX', 'A', 'Pending', '0000000000'),
    ('Aradhya', 'Mittal', 'IX', 'A', 'Pending', '0000000000'),
    ('Aarav', 'Mittal', 'IX', 'A', 'Pending', '0000000000'),
    ('Aayush', 'Jain', 'IX', 'A', 'Pending', '0000000000')
]

# Insert all students at once
cursor.executemany('''
    INSERT INTO Students (first_name, last_name, class_level, batch_section, parent_name, parent_phone) 
    VALUES (?, ?, ?, ?, ?, ?)
''', students)

conn.commit()
conn.close()
print("All Class IX students added successfully!")
