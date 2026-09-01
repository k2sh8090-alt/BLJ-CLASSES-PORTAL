from flask import Flask, request, render_template_string, redirect, session, url_for
import psycopg2
import hashlib
import os

app = Flask(__name__)
# Session key required for Flask login state
app.secret_key = "blj_classes_secure_key_2026" 

def get_connection():
    # Connects to Supabase using the URL stored in Vercel's Environment Variables
    db_url = os.environ.get("DATABASE_URL")
    if not db_url:
        raise ValueError("DATABASE_URL environment variable is missing in Vercel.")
    return psycopg2.connect(db_url)

# --- HTML TEMPLATES ---
LOGIN_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>BLJ Classes | Login</title>
    <style>
        body { font-family: sans-serif; background-color: #0f172a; color: white; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .box { background-color: #1e293b; padding: 40px; border-radius: 10px; text-align: center; width: 320px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); }
        input { margin: 10px 0; padding: 12px; width: 90%; border-radius: 5px; border: 1px solid #334155; background-color: #0f172a; color: white; }
        button { background-color: #3b82f6; color: white; padding: 12px; border: none; width: 98%; border-radius: 5px; cursor: pointer; font-weight: bold; margin-top: 10px; }
        button:hover { background-color: #2563eb; }
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
        {% if error %}<p style="color:#ef4444; font-size: 14px; margin-top: 15px;">⚠️ {{ error }}</p>{% endif %}
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
        body { font-family: sans-serif; background-color: #0f172a; color: white; padding: 40px; margin: 0; }
        .card { background-color: #1e293b; padding: 25px; border-radius: 8px; margin-bottom: 20px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); }
        table { width: 100%; border-collapse: collapse; margin-top: 15px; }
        th, td { padding: 12px; border-bottom: 1px solid #334155; text-align: left; }
        th { color: #94a3b8; }
        a.logout-btn { background-color: #ef4444; color: white; text-decoration: none; font-weight: bold; padding: 8px 16px; border-radius: 5px; }
        a.logout-btn:hover { background-color: #dc2626; }
    </style>
</head>
<body>
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px;">
        <h2 style="margin: 0;">👨‍🏫 BLJ Classes Dashboard</h2>
        <a href="/logout" class="logout-btn">LOGOUT</a>
    </div>
    
    <div class="card">
        <h3 style="margin-top: 0;">Enrolled Students Overview</h3>
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

ERROR_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Connection Error</title>
</head>
<body style="font-family: sans-serif; background-color: #0f172a; color: white; padding: 40px; height: 100vh; display: flex; justify-content: center; align-items: center;">
    <div style="background-color: #1e293b; padding: 30px; border-radius: 10px; max-width: 600px; text-align: left; border: 1px solid #ef4444;">
        <h2 style="color: #ef4444; margin-top: 0;">🚨 Database Connection Failed</h2>
        <p>Vercel successfully loaded the application, but it crashed while attempting to connect to Supabase.</p>
        <div style="background-color: #0f172a; padding: 15px; border-radius: 5px; font-family: monospace; color: #f8fafc; overflow-wrap: break-word;">
            {{ error_details }}
        </div>
        <p style="color: #94a3b8; font-size: 14px; margin-top: 20px;">Please check the <strong>DATABASE_URL</strong> in your Vercel Environment Variables and verify your Supabase password is correct.</p>
        <a href='/logout' style="color: #3b82f6; text-decoration: none; font-weight: bold; display: inline-block; margin-top: 10px;">← Return to Login</a>
    </div>
</body>
</html>
"""

# --- EXPANDED ROUTING & LOGIC ---
@app.route("/", methods=["GET", "POST"])
@app.route("/api", methods=["GET", "POST"])
@app.route("/api/", methods=["GET", "POST"])
@app.route("/api/index.py", methods=["GET", "POST"])
def login():
    if session.get("authenticated"):
        return redirect(url_for("dashboard"))
        
    error = None
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        # 1. Hardcoded bypass check
        if username == "BLJclassess" and password == "classesBLJ123":
            session["authenticated"] = True
            return redirect(url_for("dashboard"))
        
        # 2. Database verification fallback
        try:
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
        except Exception as e:
            return render_template_string(ERROR_HTML, error_details=str(e))
            
    return render_template_string(LOGIN_HTML, error=error)

@app.route("/dashboard")
@app.route("/api/dashboard")
def dashboard():
    if not session.get("authenticated"):
        return redirect(url_for("login"))
        
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT student_id, first_name, last_name, class_level, subject FROM Students ORDER BY class_level, first_name")
                students = cursor.fetchall()
                
        return render_template_string(DASHBOARD_HTML, students=students)
    except Exception as e:
        return render_template_string(ERROR_HTML, error_details=str(e))

@app.route("/logout")
@app.route("/api/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
