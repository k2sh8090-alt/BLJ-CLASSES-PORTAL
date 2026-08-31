import sqlite3
import matplotlib.pyplot as plt
from fpdf import FPDF
import os

# 1. Fetch Data from SQLite
conn = sqlite3.connect('blj_classes.db')
cursor = conn.cursor()

cursor.execute("SELECT first_name, last_name, parent_name, class_level FROM Students WHERE student_id = 1")
student = cursor.fetchone()
student_name = f"{student[0]} {student[1]}"
parent_name = student[2]
class_lvl = student[3]

cursor.execute('''
    SELECT te.exam_type, tr.marks_obtained, te.max_marks
    FROM Test_Results tr
    JOIN Tests_Exams te ON tr.test_id = te.test_id
    WHERE tr.student_id = 1
''')
results = cursor.fetchall()
conn.close()

# 2. Generate the Matplotlib Chart
exams = [row[0] for row in results]
percentages = [(row[1] / row[2]) * 100 for row in results]

plt.figure(figsize=(6, 4))
plt.bar(exams, percentages, color=['#4CAF50', '#2196F3'], width=0.4)
plt.ylim(0, 100)
plt.ylabel('Score (%)')
plt.title(f'Academic Progress: {student_name}')
plt.grid(axis='y', linestyle='--', alpha=0.7)
chart_filename = 'progress_chart.png'
plt.savefig(chart_filename)
plt.close()

# 3. Create the PDF Report Card
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", 'B', 16)

# Header
pdf.cell(200, 10, txt="BLJ Classes - Academic Report", ln=True, align='C')
pdf.set_font("Arial", size=12)
pdf.cell(200, 10, txt="---------------------------------------------------------", ln=True, align='C')

# Student Details
pdf.cell(200, 10, txt=f"Dear {parent_name},", ln=True)
pdf.cell(200, 10, txt=f"Here is the latest academic update for {student_name} (Class {class_lvl}).", ln=True)
pdf.ln(10)

# Add the Chart
pdf.image(chart_filename, x=50, y=60, w=110)

# Export PDF
pdf_filename = f"{student[0]}_ReportCard.pdf"
pdf.output(pdf_filename)

# Clean up the temporary image file
os.remove(chart_filename)

print(f"Success! {pdf_filename} has been generated in your folder.")
