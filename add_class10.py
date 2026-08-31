import sqlite3

conn = sqlite3.connect('blj_classes.db')
cursor = conn.cursor()

# 45 students with specific subject tracking in the batch_section column
students = [
    ('Aadit', 'Goyal', 'X', 'Maths, Science, SST', 'Pending', '0000000000'),
    ('Aakansha', 'Krishna', 'X', 'Maths, Science', 'Pending', '0000000000'),
    ('Aanya', 'soni', 'X', 'Maths, Science', 'Pending', '0000000000'),
    ('Aarav', 'Mehra', 'X', 'Maths, Science', 'Pending', '0000000000'),
    ('Aarav', 'Sethi', 'X', 'Maths, Science', 'Pending', '0000000000'),
    ('Aarush', 'Rawat', 'X', 'Maths, Science', 'Pending', '0000000000'),
    ('Aaryan', 'Sethi', 'X', 'Maths, Science', 'Pending', '0000000000'),
    ('Aashna', 'sharma', 'X', 'Maths, Science', 'Pending', '0000000000'),
    ('Aditya', 'Jangid', 'X', 'Maths, Science', 'Pending', '0000000000'),
    ('Advik', 'Mittal', 'X', 'Maths, Science', 'Pending', '0000000000'),
    ('Anav', 'Kumawat', 'X', 'Maths, Science', 'Pending', '0000000000'),
    ('Ariana', 'bari', 'X', 'Maths, Science', 'Pending', '0000000000'),
    ('Arnav', 'Sharma', 'X', 'Maths, Science', 'Pending', '0000000000'),
    ('Arnav', 'Sharma (16)', 'X', 'Maths, Science', 'Pending', '0000000000'),
    ('Avani', 'ojha', 'X', 'Maths, Science', 'Pending', '0000000000'),
    ('Bhawika', 'sharma', 'X', 'Maths, Science', 'Pending', '0000000000'),
    ('Chahak', 'Sain', 'X', 'Maths, Science', 'Pending', '0000000000'),
    ('Devan', 'Pancholi', 'X', 'Maths, Science', 'Pending', '0000000000'),
    ('Devik', 'Chamoli', 'X', 'Maths, Science', 'Pending', '0000000000'),
    ('Devyansh', 'sharma', 'X', 'Maths, Science', 'Pending', '0000000000'),
    ('Gunjan', 'Yadav', 'X', 'Maths, Science, SST', 'Pending', '0000000000'),
    ('Harsh', 'Yadav', 'X', 'Maths, Science', 'Pending', '0000000000'),
    ('Harshit', 'budania', 'X', 'Maths, Science', 'Pending', '0000000000'),
    ('Jaanesh', 'babel', 'X', 'Maths, Science, SST', 'Pending', '0000000000'),
    ('Kabir', 'Sharma', 'X', 'Maths, Science', 'Pending', '0000000000'),
    ('Kanish', 'bhagera', 'X', 'Maths, Science', 'Pending', '0000000000'),
    ('Krisha', 'mathur', 'X', 'Maths, Science', 'Pending', '0000000000'),
    ('Mahi', 'Sharma', 'X', 'Maths, Science', 'Pending', '0000000000'),
    ('Mahika', 'Bothra', 'X', 'Maths, Science', 'Pending', '0000000000'),
    ('Manan', 'sharma', 'X', 'Maths, Science', 'Pending', '0000000000'),
    ('Manasv', 'Singh Rajawat', 'X', 'Maths, Science', 'Pending', '0000000000'),
    ('Naitik', 'Dalmia', 'X', 'Maths, Science', 'Pending', '0000000000'),
    ('Navya', 'garg', 'X', 'Maths, Science', 'Pending', '0000000000'),
    ('Parth', 'Sharma', 'X', 'Maths, Science', 'Pending', '0000000000'),
    ('Prerak', 'Jain', 'X', 'Maths, Science', 'Pending', '0000000000'),
    ('Rajvi', 'Mamoria', 'X', 'Maths, Science', 'Pending', '0000000000'),
    ('Rebecca', 'samuel', 'X', 'Maths, Science', 'Pending', '0000000000'),
    ('Risha', 'Agarwal', 'X', 'Maths, Science', 'Pending', '0000000000'),
    ('Rishabh', 'jain', 'X', 'Maths, Science', 'Pending', '0000000000'),
    ('Sadhana', 'Mahawar', 'X', 'Maths, Science', 'Pending', '0000000000'),
    ('Shiksha', 'Sharma', 'X', 'Maths, Science', 'Pending', '0000000000'),
    ('Shivi', 'Sharma', 'X', 'Maths, Science', 'Pending', '0000000000'),
    ('Shristhi', 'Nangalia', 'X', 'Maths, Science', 'Pending', '0000000000'),
    ('Shubham', 'Agarwal', 'X', 'Maths, Science', 'Pending', '0000000000'),
    ('Siddharth', 'kumar', 'X', 'Maths, Science', 'Pending', '0000000000')
]

cursor.executemany('''
    INSERT INTO Students (first_name, last_name, class_level, batch_section, parent_name, parent_phone) 
    VALUES (?, ?, ?, ?, ?, ?)
''', students)

conn.commit()
conn.close()
print("All Class X students added successfully!")