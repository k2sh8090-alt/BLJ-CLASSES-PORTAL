import os
import sys

# Add root directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_GET(self):from flask import Flask, request, render_template_string, redirect, session, url_for
import psycopg2
import hashlib
import os

app = Flask(__name__)
# Session key required for Flask login state
app.secret_key = "blj_classes_secure_key_2026" 

def get_connection():
    return psycopg2.connect(os.environ.get("DATABASE_URL"))

# --- HTML TEMPLATES ---
LOGIN_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>BLJ Classes | Login</title>
    <style>
        body { font-family: sans-serif; background-color: #0f172a; color: white; display: flex; justify-content: center; align-items: center; height: 100vh; }
        .box { background-color: #1e293b; padding: 40px; border-radius: 10px; text-align: center; }
        input { margin: 10px 0; padding: 10px; width: 90%; border-radius: 5px; border: none; }
        button { background-color: #3b82f6; color: white; padding: 10px; border: none; width: 95%; border-radius: 5px; cursor: pointer; font-weight: bold; }
    </style>
</head>
<body>
    <div class="box">
        <h2>🎓 BLJ Classes Portal</h2>
        <form method="POST">
            <input type="text" name="username" placeholder="Username" required><br>
            <input type="password" name="password" placeholder="Password" required><br>
            <button type="submit">🔒 Secure Login</button>
        </form>
        {% if error %}<p style="color:#ef4444;">⚠️ {{ error }}</p>{% endif %}
    </div>
</body>
</html>
"""

DASHBOARD_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>BLJ Classes | Dashboard</title>
    <style>
        body { font-family: sans-serif; background-color: #0f172a; color: white; padding: 40px; }
        .card { background-color: #1e293b; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
        table { width: 100%; border-collapse: collapse; margin-top: 15px; }
        th, td { padding: 10px; border-bottom: 1px solid #334155; text-align: left; }
        a { color: #ef4444; text-decoration: none; font-weight: bold; }
    </style>
</head>
<body>
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <h2>👨‍🏫 BLJ Classes Dashboard</h2>
        <a href="/logout">LOGOUT</a>
    </div>
    
    <div class="card">
        <h3>Enrolled Students Overview</h3>
        <table>
            <tr><th>ID</th><th>First Name</th><th>Last Name</th><th>Class</th><th>Subject</th></tr>
            {% for student in students %}
            <tr>
                <td>{{ student[0] }}</td><td>{{ student[1] }}</td><td>{{ student[2] }}</td>
                <td>{{ student[3] }}</td><td>{{ student[4] }}</td>
            </tr>
            {% endfor %}
        </table>
    </div>
</body>
</html>
"""

# --- ROUTING & LOGIC ---
@app.route("/", methods=["GET", "POST"])
def login():
    if session.get("authenticated"):
        return redirect(url_for("dashboard"))
        
    error = None
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        # Hardcoded bypass check matching your preferences
        if username == "BLJclassess" and password == "classesBLJ123":
            session["authenticated"] = True
            return redirect(url_for("dashboard"))
        
        # Database verification fallback
        with get_connection() as conn:
            with conn.cursor() as cursor:
                pass_hash = hashlib.sha256(password.encode()).hexdigest()
                cursor.execute("SELECT * FROM Teachers WHERE username = %s AND password_hash = %s", (username, pass_hash))
                user = cursor.fetchone()
        
        if user:
            session["authenticated"] = True
            return redirect(url_for("dashboard"))
        else:
            error = "Invalid credentials provided."
            
    return render_template_string(LOGIN_HTML, error=error)

@app.route("/dashboard")
def dashboard():
    if not session.get("authenticated"):
        return redirect(url_for("login"))
        
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT student_id, first_name, last_name, class_level, subject FROM Students ORDER BY class_level, first_name")
            students = cursor.fetchall()
            
    return render_template_string(DASHBOARD_HTML, students=students)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        
        html_content = """
        <!DOCTYPE html>
        <html>
            <head>
                <title>BLJ Classes Portal</title>
            </head>
            <body style="font-family: Arial, sans-serif; text-align: center; margin-top: 80px; background-color: #0f172a; color: #f8fafc;">
                <h2>BLJ Classes Portal</h2>
                <p>Serverless environment initialized on Vercel.</p>
                <p style="color: #94a3b8; font-size: 14px;">Note: Streamlit apps require a persistent websocket server process.</p>
            </body>
        </html>
        """
        self.wfile.write(html_content.encode('utf-8'))
        return

    def do_POST(self):
        self.do_GET()
