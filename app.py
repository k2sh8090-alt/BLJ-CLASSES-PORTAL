import streamlit as st
import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF
import os
import datetime
import urllib.parse
import hashlib

# --- PAGE CONFIGURATION & ENTERPRISE STYLING ---
st.set_page_config(
    page_title="BLJ Classes | Enterprise Faculty Portal", 
    page_icon="🎓", 
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .main { background-color: var(--background-color); }
    div[data-testid="stMetric"] {
        background-color: var(--secondary-background-color, #1e293b);
        border: 1px solid #334155;
        padding: 15px 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    div[data-testid="stMetric"] label { color: #94a3b8 !important; }
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] { color: #f8fafc !important; }
    h1, h2, h3 { color: #f8fafc; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
    [data-testid="stSidebar"] { background-color: #0f172a; color: #ffffff; }
    [data-testid="stSidebar"] label, [data-testid="stSidebar"] .stMarkdown { color: #e2e8f0; }
    
    div[data-testid="stSidebar"] button {
        color: black !important;
        font-weight: 600 !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- CLOUD DATABASE CONNECTION ---
def get_connection():
    db_url = st.secrets["DATABASE_URL"]
    return psycopg2.connect(db_url)

def init_normalized_db():
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Teachers (
                    teacher_id SERIAL PRIMARY KEY,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL
                );
            ''')
            cursor.execute('''
                INSERT INTO Teachers (username, password_hash) 
                VALUES (%s, %s)
                ON CONFLICT (username) DO NOTHING;
            ''', ("BLJclasses", hashlib.sha256("classesBLJ123".encode()).hexdigest()))
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Classes (
                    class_id SERIAL PRIMARY KEY,
                    class_level TEXT UNIQUE NOT NULL
                );
            ''')
            for cls in ["IX", "X", "XI", "XII"]:
                cursor.execute("INSERT INTO Classes (class_level) VALUES (%s) ON CONFLICT (class_level) DO NOTHING;", (cls,))

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Students (
                    student_id SERIAL PRIMARY KEY,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    class_level TEXT NOT NULL,
                    subject TEXT NOT NULL,
                    parent_relation TEXT,
                    parent_phone TEXT NOT NULL,
                    CONSTRAINT unq_student UNIQUE (first_name, last_name, class_level)
                );
            ''')

            # Clean Roster Seed Data
            students_roster = [
                ("Tanav", "Sharma", "IX", "Maths, Science", "Father", "9876543201"),
                ("Nevin", "", "IX", "Maths, Science", "Father", "9876543202"),
                ("Ronav", "Moolwani", "IX", "Maths, Science", "Father", "9876543203"),
                ("Hridyansh", "Gupta", "IX", "Maths, Science", "Father", "9876543204"),
                ("Sourish", "Gupta", "IX", "Maths, Science", "Father", "9876543205"),
                ("Parinidhi", "Agarwal", "IX", "Maths, Science", "Father", "9876543206"),
                ("Akshita", "Sethi", "IX", "Maths, Science", "Father", "9876543207"),
                ("Tejasvi", "Gehlot", "IX", "Maths, Science", "Father", "9876543208"),
                ("Jinal", "Jangid", "IX", "Maths, Science", "Father", "9876543209"),
                ("Aradhya", "Mittal", "IX", "Maths, Science", "Father", "9876543210"),
                ("Aarav", "Mittal", "IX", "Maths, Science", "Father", "9876543211"),
                ("Aayush", "Jain", "IX", "Maths, Science", "Father", "9876543212"),
                ("Aadit", "Goyal", "X", "Maths, Science, SST", "Father", "9876543220"),
                ("Gunjan", "Yadav", "X", "Maths, Science, SST", "Father", "9876543221"),
                ("Jaanesh", "Babel", "X", "Maths, Science, SST", "Father", "9876543222"),
                ("Aakansha", "Krishna", "X", "Maths, Science", "Father", "9876543223"),
                ("Aanya", "Soni", "X", "Maths, Science", "Father", "9876543224"),
                ("Aarav", "Mehra", "X", "Maths, Science", "Father", "9876543225"),
                ("Aarav", "Sethi", "X", "Maths, Science", "Father", "9876543226"),
                ("Aarush", "Rawat", "X", "Maths, Science", "Father", "9876543227"),
                ("Aaryan", "Sethi", "X", "Maths, Science", "Father", "9876543228"),
                ("Aashna", "Sharma", "X", "Maths, Science", "Father", "9876543229"),
                ("Aditya", "Jangid", "X", "Maths, Science", "Father", "9876543230"),
                ("Advik", "Mittal", "X", "Maths, Science", "Father", "9876543231"),
                ("Anav", "Kumawat", "X", "Maths, Science", "Father", "9876543232"),
                ("Ariana", "Bari", "X", "Maths, Science", "Father", "9876543233"),
                ("Arnav", "Sharma", "X", "Maths, Science", "Father", "9876543234"),
                ("Arnav", "Sharma (16)", "X", "Maths, Science", "Father", "9876543235"),
                ("Avani", "Ojha", "X", "Maths, Science", "Father", "9876543236"),
                ("Bhawika", "Sharma", "X", "Maths, Science", "Father", "9876543237"),
                ("Chahak", "Sain", "X", "Maths, Science", "Father", "9876543238"),
                ("Devan", "Pancholi", "X", "Maths, Science", "Father", "9876543239"),
                ("Devik", "Chamoli", "X", "Maths, Science", "Father", "9876543240"),
                ("Devyansh", "Sharma", "X", "Maths, Science", "Father", "9876543241"),
                ("Harsh", "Yadav", "X", "Maths, Science", "Father", "9876543242"),
                ("Harshit", "Budania", "X", "Maths, Science", "Father", "9876543243"),
                ("Kabir", "Sharma", "X", "Maths, Science", "Father", "9876543244"),
                ("Kanish", "Bhagera", "X", "Maths, Science", "Father", "9876543245"),
                ("Krisha", "Mathur", "X", "Maths, Science", "Father", "9876543246"),
                ("Mahi", "Sharma", "X", "Maths, Science", "Father", "9876543247"),
                ("Mahika", "Bothra", "X", "Maths, Science", "Father", "9876543248"),
                ("Manan", "Sharma", "X", "Maths, Science", "Father", "9876543249"),
                ("Manasv Singh", "Rajawat", "X", "Maths, Science", "Father", "9876543250"),
                ("Naitik", "Dalmia", "X", "Maths, Science", "Father", "9876543251"),
                ("Navya", "Garg", "X", "Maths, Science", "Father", "9876543252"),
                ("Parth", "Sharma", "X", "Maths, Science", "Father", "9876543253"),
                ("Prerak", "Jain", "X", "Maths, Science", "Father", "9876543254"),
                ("Rajvi", "Mamoria", "X", "Maths, Science", "Father", "9876543255"),
                ("Rebecca", "Samuel", "X", "Maths, Science", "Father", "9876543256"),
                ("Risha", "Agarwal", "X", "Maths, Science", "Father", "9876543257"),
                ("Rishabh", "Jain", "X", "Maths, Science", "Father", "9876543258"),
                ("Sadhana", "Mahawar", "X", "Maths, Science", "Father", "9876543259"),
                ("Shiksha", "Sharma", "X", "Maths, Science", "Father", "9876543260"),
                ("Shivi", "Sharma", "X", "Maths, Science", "Father", "9876543261"),
                ("Shristhi", "Nangalia", "X", "Maths, Science", "Father", "9876543262"),
                ("Shubham", "Agarwal", "X", "Maths, Science", "Father", "9876543263"),
                ("Siddharth", "Kumar", "X", "Maths, Science", "Father", "9876543264")
            ]
            
            for s in students_roster:
                cursor.execute('''
                    INSERT INTO Students (first_name, last_name, class_level, subject, parent_relation, parent_phone)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT (first_name, last_name, class_level) DO NOTHING;
                ''', s)

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Subjects (
                    subject_id SERIAL PRIMARY KEY,
                    subject_name TEXT NOT NULL,
                    class_level TEXT NOT NULL
                );
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Tests_Exams (
                    test_id SERIAL PRIMARY KEY,
                    subject_id INTEGER REFERENCES Subjects(subject_id),
                    exam_type TEXT NOT NULL,
                    exam_date DATE NOT NULL,
                    max_marks INTEGER NOT NULL,
                    chapter_name TEXT
                );
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Test_Results (
                    result_id SERIAL PRIMARY KEY,
                    test_id INTEGER REFERENCES Tests_Exams(test_id),
                    student_id INTEGER REFERENCES Students(student_id),
                    marks_obtained REAL,
                    teacher_feedback TEXT
                );
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Attendance (
                    attendance_id SERIAL PRIMARY KEY,
                    student_id INTEGER REFERENCES Students(student_id),
                    date DATE NOT NULL,
                    status TEXT NOT NULL
                );
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Assignments (
                    assignment_id SERIAL PRIMARY KEY,
                    class_level TEXT NOT NULL,
                    subject TEXT NOT NULL DEFAULT 'Maths (Core)',
                    title TEXT NOT NULL,
                    due_date DATE NOT NULL,
                    resource_link TEXT
                );
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Assignment_Submissions (
                    submission_id SERIAL PRIMARY KEY,
                    assignment_id INTEGER REFERENCES Assignments(assignment_id),
                    student_id INTEGER REFERENCES Students(student_id),
                    status TEXT NOT NULL,
                    remarks TEXT,
                    CONSTRAINT unq_asg_sub UNIQUE (assignment_id, student_id)
                );
            ''')
        conn.commit()

init_normalized_db()

# --- AUTHENTICATION GATE ---
def check_password():
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False
    if st.session_state["authenticated"]:
        return True

    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("## 🎓 BLJ Classes")
        st.markdown("### Secure Faculty Portal Authentication")
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            if st.form_submit_button("🔒 Secure Login", use_container_width=True):
                if username == "BLJclasses" and password == "classesBLJ123":
                    st.session_state["authenticated"] = True
                    st.rerun()
                else:
                    with get_connection() as conn:
                        with conn.cursor() as cursor:
                            pass_hash = hashlib.sha256(password.encode()).hexdigest()
                            cursor.execute("SELECT * FROM Teachers WHERE username = %s AND password_hash = %s", (username, pass_hash))
                            user = cursor.fetchone()
                    if user:
                        st.session_state["authenticated"] = True
                        st.rerun()
                    else:
                        st.error("⚠️ Invalid credentials provided.")
    return False

if not check_password():
    st.stop()

# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    if os.path.exists("logo.png"):
        st.image("logo.png", use_container_width=True)
    else:
        st.markdown("## 🎓 BLJ Classes")
    
    st.markdown("---")
    menu = [
        "🏠 Dashboard", 
        "👥 View Students", 
        "➕ Add Student", 
        "📅 Mark Attendance", 
        "📈 Manage Tests", 
        "📚 Assignments", 
        "📢 Broadcasts", 
        "🖨️ Report Cards", 
        "📊 Class Overview"
    ]
    choice = st.selectbox("Navigation Menu", menu, label_visibility="collapsed")
    
    st.markdown("<br>" * 10, unsafe_allow_html=True)
    _, logout_col = st.columns([1, 1.2])
    with logout_col:
        if st.button("LOGOUT", use_container_width=True):
            st.session_state["authenticated"] = False
            st.rerun()

st.title("👨‍🏫 BLJ Classes - Enterprise Teacher Portal")
st.markdown("---")

CLASS_LEVELS = ["IX", "X", "XI", "XII"]

# --- 0. DASHBOARD ---
if choice == "🏠 Dashboard":
    st.subheader("Executive Operational Summary & Institute Health")
    with get_connection() as conn:
        total_students = pd.read_sql_query("SELECT COUNT(*) as count FROM Students", conn).iloc[0]['count']
        total_tests = pd.read_sql_query("SELECT COUNT(*) as count FROM Tests_Exams", conn).iloc[0]['count']
        today_att = pd.read_sql_query(f"SELECT COUNT(*) as count FROM Attendance WHERE date = '{datetime.date.today()}' AND status = 'Present'", conn).iloc[0]['count']
        total_assignments = pd.read_sql_query("SELECT COUNT(*) as count FROM Assignments", conn).iloc[0]['count']
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Enrolled Students", total_students)
    col2.metric("Evaluations Conducted", total_tests)
    col3.metric("Present Today", today_att)
    col4.metric("Active Assignments", total_assignments)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.info("💡 **Cloud Synchronization Active:** Real-time data sync across all authorized devices.")

# --- 1. VIEW STUDENTS ---
elif choice == "👥 View Students":
    st.subheader("Enrolled Students Directory & Management")
    search_term = st.text_input("🔍 Global Student Directory Search")
    tabs = st.tabs(["All Classes"] + [f"Class {c}" for c in CLASS_LEVELS])
    
    with get_connection() as conn:
        for i, tab in enumerate(tabs):
            with tab:
                c_filter = "All" if i == 0 else CLASS_LEVELS[i-1]
                q = "SELECT student_id, first_name, last_name, class_level, subject, parent_relation, parent_phone FROM Students" if c_filter == "All" else f"SELECT student_id, first_name, last_name, class_level, subject, parent_relation, parent_phone FROM Students WHERE class_level = '{c_filter}'"
                df = pd.read_sql_query(q, conn)
                
                if not df.empty:
                    df.insert(0, "Class ID", [f"{r['class_level']}-{idx:02d}" for idx, r in df.iterrows()])
                    att_list = []
                    for sid in df['student_id']:
                        att = pd.read_sql_query(f"SELECT (SUM(CASE WHEN status='Present' THEN 1 ELSE 0.0 END) / COUNT(*)) * 100 AS att FROM Attendance WHERE student_id = {sid}", conn).iloc[0]['att']
                        att_list.append(f"{att:.1f}%" if pd.notnull(att) else "No Records")
                    df['Overall Attendance'] = att_list
                
                if search_term:
                    df = df[df['first_name'].str.contains(search_term, case=False) | df['last_name'].str.contains(search_term, case=False)]
                
                if df.empty:
                    st.info("No records found.")
                else:
                    edited = st.data_editor(df.drop(columns=["student_id"]), hide_index=True, disabled=["Class ID", "Overall Attendance"], use_container_width=True, key=f"ed_{c_filter}")
                    
                    col_save, col_del = st.columns([1, 1])
                    with col_save:
                        if st.button("💾 Commit Updates", key=f"sv_{c_filter}", use_container_width=True):
                            with conn.cursor() as cursor:
                                for idx, row in edited.iterrows():
                                    orig_id = df.loc[df.index == idx, 'student_id'].values[0]
                                    cursor.execute("UPDATE Students SET first_name=%s, last_name=%s, class_level=%s, subject=%s, parent_relation=%s, parent_phone=%s WHERE student_id=%s", 
                                        (row['first_name'], row['last_name'], row['class_level'], row['subject'], row['parent_relation'], row['parent_phone'], int(orig_id)))
                            conn.commit()
                            st.toast("Synchronized successfully!", icon="🎉")
                            st.rerun()
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.markdown("#### 🗑️ Remove Student Record")
                    del_options = {f"{row['Class ID']} - {row['first_name']} {row['last_name']}": row['student_id'] for _, row in df.iterrows()}
                    selected_del_label = st.selectbox("Select Student to Delete", list(del_options.keys()), key=f"del_sel_{c_filter}")
                    
                    if st.button("⚠️ Permanently Delete Student", key=f"del_btn_{c_filter}", use_container_width=True):
                        target_student_id = int(del_options[selected_del_label])
                        with conn.cursor() as cursor:
                            cursor.execute("DELETE FROM Test_Results WHERE student_id = %s", (target_student_id,))
                            cursor.execute("DELETE FROM Attendance WHERE student_id = %s", (target_student_id,))
                            cursor.execute("DELETE FROM Assignment_Submissions WHERE student_id = %s", (target_student_id,))
                            cursor.execute("DELETE FROM Students WHERE student_id = %s", (target_student_id,))
                        conn.commit()
                        st.toast("Student record permanently removed.", icon="🗑️")
                        st.rerun()

# --- 2. ADD STUDENT ---
elif choice == "➕ Add Student":
    st.subheader("New Student Admission Onboarding")
    with st.form("add_student_form", clear_on_submit=True):
        cls = st.selectbox("Class Level", CLASS_LEVELS)
        col1, col2 = st.columns(2)
        with col1:
            fname = st.text_input("First Name *")
            prelation = st.selectbox("Parent Relation", ["Father", "Mother", "Guardian"])
        with col2:
            lname = st.text_input("Last Name *")
            default_sub = "Maths, Science" if cls == "IX" else ("Maths, Science, SST" if cls == "X" else "Maths (Core)")
            subject = st.text_input("Enrolled Subject(s)", value=default_sub)
            pphone = st.text_input("Parent Phone Number *")
            
        if st.form_submit_button("📥 Register Student", use_container_width=True):
            if not fname or not lname or not pphone:
                st.error("⚠️ Mandatory fields cannot be empty.")
            else:
                with get_connection() as conn:
                    with conn.cursor() as cursor:
                        cursor.execute("INSERT INTO Students (first_name, last_name, class_level, subject, parent_relation, parent_phone) VALUES (%s, %s, %s, %s, %s, %s)",
                            (fname, lname, cls, subject, prelation, pphone))
                    conn.commit()
                st.success(f"Registered {fname} {lname} successfully.")

# --- 3. MARK ATTENDANCE & COMPLIANCE ---
elif choice == "📅 Mark Attendance":
    st.subheader("Daily Attendance Register & Compliance Panel")
    mode = st.radio("Mode", ["📝 Record Register", "📅 Audit Logs", "⚠️ Attendance Shortage & Debarment"], horizontal=True)
    
    with get_connection() as conn:
        if mode == "⚠️ Attendance Shortage & Debarment":
            st.markdown("### 🚫 Institutional Attendance Debarment Report (< 75% Cutoff)")
            sel_debar_cls = st.selectbox("Select Class for Debarment Check", CLASS_LEVELS, key="debar_cls")
            
            debar_query = f'''
                SELECT s.student_id, s.first_name || ' ' || s.last_name AS Student_Name, s.parent_phone,
                       (SELECT COUNT(*) FROM Attendance WHERE student_id = s.student_id) as total_days,
                       (SELECT COUNT(*) FROM Attendance WHERE student_id = s.student_id AND status = 'Present') as present_days
                FROM Students s WHERE s.class_level = '{sel_debar_cls}'
            '''
            d_df = pd.read_sql_query(debar_query, conn)
            
            if d_df.empty:
                st.info("No student records available for this class.")
            else:
                rates = []
                statuses = []
                for _, row in d_df.iterrows():
                    t = row['total_days']
                    p = row['present_days']
                    rate = (p / t * 100) if t > 0 else 100.0
                    rates.append(f"{rate:.1f}%")
                    statuses.append("🚨 Debarred (< 75%)" if rate < 75.0 else "✅ Eligible")
                
                d_df['Attendance Rate'] = rates
                d_df['Status'] = statuses
                
                display_d_df = d_df[['Student_Name', 'total_days', 'present_days', 'Attendance Rate', 'Status']]
                st.dataframe(display_d_df, hide_index=True, use_container_width=True)
                
                st.markdown("---")
                st.markdown("#### 💬 Deficit Notice Actions")
                debarred_students = d_df[d_df['Status'].str.contains("Debarred")]
                if debarred_students.empty:
                    st.success("🎉 All students in this class meet the 75% attendance criteria!")
                else:
                    for _, row in debarred_students.iterrows():
                        msg = f"Dear Parent, your ward {row['Student_Name']} has an attendance rate of {row['Attendance Rate']}, which falls below the mandatory 75% requirement."
                        st.markdown(f"- **{row['Student_Name']}** ({row['Attendance Rate']}): [💬 Send Shortage Notice via WhatsApp](https://wa.me/{row['parent_phone']}?text={urllib.parse.quote(msg)})", unsafe_allow_html=True)
        
        else:
            st.markdown("### 📊 Class-wise Daily Attendance & End-of-Day Briefing")
            summary_date = st.date_input("Select Summary Date", datetime.date.today(), key="summary_date_picker")
            
            summary_data = []
            for cls in CLASS_LEVELS:
                total_cls = pd.read_sql_query(f"SELECT COUNT(*) as cnt FROM Students WHERE class_level = '{cls}'", conn).iloc[0]['cnt']
                present_cls = pd.read_sql_query(f'''
                    SELECT COUNT(*) as cnt FROM Attendance a 
                    JOIN Students s ON a.student_id = s.student_id 
                    WHERE s.class_level = '{cls}' AND a.date = '{summary_date}' AND a.status = 'Present'
                ''', conn).iloc[0]['cnt']
                
                absent_cls = total_cls - present_cls
                pct = f"{(present_cls / total_cls * 100):.1f}%" if total_cls > 0 else "0.0%"
                summary_data.append({
                    "Class Level": f"Class {cls}",
                    "Present": present_cls,
                    "Absent": absent_cls,
                    "Total Enrolled": total_cls,
                    "Attendance Rate": pct
                })
            
            summary_df = pd.DataFrame(summary_data)
            st.dataframe(summary_df, hide_index=True, use_container_width=True)
            st.markdown("---")

            selected_class = st.selectbox("Select Target Class for Register/Audit", CLASS_LEVELS, key="att_cls")
            
            if mode == "📝 Record Register":
                s_df = pd.read_sql_query(f"SELECT student_id, first_name, last_name FROM Students WHERE class_level = '{selected_class}'", conn)
                if s_df.empty:
                    st.warning("No students in this class.")
                else:
                    with st.form("att_form"):
                        date = st.date_input("Register Date", datetime.date.today())
                        states = {row['student_id']: st.checkbox(f"{row['first_name']} {row['last_name']}", value=True) for _, row in s_df.iterrows()}
                        if st.form_submit_button("💾 Save Attendance"):
                            with conn.cursor() as cursor:
                                for sid, present in states.items():
                                    cursor.execute("INSERT INTO Attendance (student_id, date, status) VALUES (%s, %s, %s)", (sid, date, "Present" if present else "Absent"))
                            conn.commit()
                            st.toast("Attendance saved!", icon="✅")
            else:
                date = st.date_input("Audit Date", datetime.date.today())
                query = f'''
                    SELECT s.first_name || ' ' || s.last_name AS "Student Name", a.status AS "Status", s.parent_phone AS "Phone"
                    FROM Attendance a JOIN Students s ON a.student_id = s.student_id
                    WHERE s.class_level = '{selected_class}' AND a.date = '{date}'
                '''
                log_df = pd.read_sql_query(query, conn)
                if log_df.empty:
                    st.info("No attendance records found for this date.")
                else:
                    for _, row in log_df.iterrows():
                        c1, c2, c3 = st.columns([3, 2, 3])
                        c1.write(row['Student Name'])
                        c2.write(row['Status'])
                        if row['Status'] == 'Absent':
                            msg = f"Hello, your ward {row['Student Name']} was absent on {date}."
                            c3.markdown(f"[💬 Send Alert](https://wa.me/{row['Phone']}?text={urllib.parse.quote(msg)})", unsafe_allow_html=True)

# --- 4. MANAGE TESTS & WEAK-SPOT MAPPING ---
elif choice == "📈 Manage Tests":
    st.subheader("Evaluations & Weak-Spot Mapping Suite")
    mode = st.radio("Protocol", ["➕ Add Test", "✏️ Edit Test", "📊 Weak-Spot Analysis"], horizontal=True)
    selected_class = st.selectbox("Class", CLASS_LEVELS, key="test_cls")
    
    with get_connection() as conn:
        if mode == "➕ Add Test":
            subs = {
                "IX": ["Maths", "Science"], 
                "X": ["Maths", "Science", "SST"], 
                "XI": ["Maths (Core)", "Maths (Applied)", "Physics", "Chemistry"], 
                "XII": ["Maths (Core)", "Maths (Applied)", "Physics", "Chemistry"]
            }
            sub_name = st.selectbox("Subject", subs.get(selected_class, ["Maths (Core)"]))
            s_df = pd.read_sql_query(f"SELECT student_id, first_name, last_name FROM Students WHERE class_level = '{selected_class}'", conn)
            
            if s_df.empty:
                st.warning("No students available.")
            else:
                with st.form("test_form"):
                    chap = st.text_input("Chapter Description")
                    c1, c2 = st.columns(2)
                    with c1: etype = st.selectbox("Type", ["Weekly Test", "Mid-Term", "Final"])
                    with c2: 
                        edate = st.date_input("Date", datetime.date.today())
                        max_m = st.number_input("Max Marks", min_value=1, value=100)
                    
                    marks_map = {}
                    for _, row in s_df.iterrows():
                        sid = row['student_id']
                        sc1, sc2, sc3 = st.columns([2, 1, 2])
                        sc1.write(f"{row['first_name']} {row['last_name']}")
                        marks_map[sid] = (sc2.number_input("Marks", 0.0, step=0.5, key=f"m_{sid}", label_visibility="collapsed"),
                                          sc3.text_input("Remarks", key=f"f_{sid}", label_visibility="collapsed"))
                    
                    if st.form_submit_button("💾 Save Test & Scores"):
                        with conn.cursor() as cursor:
                            cursor.execute("SELECT subject_id FROM Subjects WHERE subject_name = %s AND class_level = %s", (sub_name, selected_class))
                            s_row = cursor.fetchone()
                            if s_row:
                                sub_id = s_row[0]
                            else:
                                cursor.execute("INSERT INTO Subjects (subject_name, class_level) VALUES (%s, %s) RETURNING subject_id", (sub_name, selected_class))
                                sub_id = cursor.fetchone()[0]
                            
                            cursor.execute("INSERT INTO Tests_Exams (subject_id, exam_type, exam_date, max_marks, chapter_name) VALUES (%s, %s, %s, %s, %s) RETURNING test_id", (sub_id, etype, edate, max_m, chap))
                            tid = cursor.fetchone()[0]
                            
                            for sid, (m, f) in marks_map.items():
                                cursor.execute("INSERT INTO Test_Results (test_id, student_id, marks_obtained, teacher_feedback) VALUES (%s, %s, %s, %s)", (tid, sid, m, f))
                        conn.commit()
                        st.toast("Scores committed successfully!", icon="✅")
        elif mode == "📊 Weak-Spot Analysis":
            st.markdown("### 📉 Chapter Performance & Weak-Spot Mapping")
            weak_query = f'''
                SELECT te.chapter_name AS Chapter, sub.subject_name AS Subject, 
                       ROUND(AVG((tr.marks_obtained * 100.0) / te.max_marks)::numeric, 2) AS Avg_Percentage
                FROM Test_Results tr 
                JOIN Tests_Exams te ON tr.test_id = te.test_id 
                JOIN Subjects sub ON te.subject_id = sub.subject_id 
                JOIN Students s ON tr.student_id = s.student_id 
                WHERE s.class_level = '{selected_class}' AND te.chapter_name IS NOT NULL AND te.chapter_name != ''
                GROUP BY te.chapter_name, sub.subject_name
            '''
            weak_df = pd.read_sql_query(weak_query, conn)
            if weak_df.empty:
                st.info("Not enough test chapter data available for analysis.")
            else:
                st.dataframe(weak_df, hide_index=True, use_container_width=True)
                st.markdown("---")
                st.markdown("#### 🚨 Chapters Requiring Immediate Remedial Focus (< 50% Average)")
                critical_chapters = weak_df[weak_df['avg_percentage'] < 50.0] if 'avg_percentage' in weak_df.columns else weak_df[weak_df['Avg_Percentage'] < 50.0]
                if critical_chapters.empty:
                    st.success("🎉 Excellent! No critical weak-spot chapters identified below the 50% threshold.")
                else:
                    for _, r in critical_chapters.iterrows():
                        ch = r['chapter'] if 'chapter' in r else r['Chapter']
                        sb = r['subject'] if 'subject' in r else r['Subject']
                        av = r['avg_percentage'] if 'avg_percentage' in r else r['Avg_Percentage']
                        st.warning(f"⚠️ **{sb} - {ch}** (Class Average: **{av}%**) requires a revision lecture.")

# --- ASSIGNMENT & HOMEWORK TRACKER ---
elif choice == "📚 Assignments":
    st.subheader("📚 Assignment & Homework Operations Panel")
    a_mode = st.radio("Action", ["➕ Create Assignment", "📋 Track Submissions", "🗑️ Delete Assignment"], horizontal=True)
    sel_cls = st.selectbox("Class Level", CLASS_LEVELS, key="asg_cls")
    
    class_subject_mapping = {
        "IX": ["Maths", "Science"],
        "X": ["Maths", "Science", "SST"],
        "XI": ["Maths (Core)", "Maths (Applied)", "Physics", "Chemistry"],
        "XII": ["Maths (Core)", "Maths (Applied)", "Physics", "Chemistry"]
    }
    allowed_subjects = class_subject_mapping.get(sel_cls, ["Maths (Core)"])
    
    with get_connection() as conn:
        if a_mode == "➕ Create Assignment":
            with st.form("create_asg"):
                asg_subject = st.selectbox("Assignment Subject", allowed_subjects)
                title = st.text_input("Assignment Title / Description")
                due = st.date_input("Due Date", datetime.date.today())
                resource_url = st.text_input("Reference Resource / Study Material Link (Optional)")
                
                if st.form_submit_button("Publish Assignment"):
                    if title:
                        with conn.cursor() as cursor:
                            cursor.execute("INSERT INTO Assignments (class_level, subject, title, due_date, resource_link) VALUES (%s, %s, %s, %s, %s) RETURNING assignment_id", (sel_cls, asg_subject, title, due, resource_url))
                            asg_id = cursor.fetchone()[0]
                            
                            students = pd.read_sql_query(f"SELECT student_id FROM Students WHERE class_level = '{sel_cls}'", conn)
                            for _, s in students.iterrows():
                                cursor.execute("INSERT INTO Assignment_Submissions (assignment_id, student_id, status, remarks) VALUES (%s, %s, %s, %s) ON CONFLICT (assignment_id, student_id) DO NOTHING", (asg_id, int(s['student_id']), "Pending", ""))
                        conn.commit()
                        st.success("Assignment published successfully!")
                    else:
                        st.error("Title cannot be blank.")
        elif a_mode == "📋 Track Submissions":
            asgs = pd.read_sql_query(f"SELECT assignment_id, subject, title, due_date, resource_link FROM Assignments WHERE class_level = '{sel_cls}'", conn)
            if asgs.empty:
                st.info("No assignments found for this class.")
            else:
                asg_opts = {f"[{r['subject']}] {r['title']} (Due: {r['due_date']})": r['assignment_id'] for _, r in asgs.iterrows()}
                selected_asg_label = st.selectbox("Select Assignment", list(asg_opts.keys()))
                asg_id = int(asg_opts[selected_asg_label])
                
                res_link = asgs.loc[asgs['assignment_id'] == asg_id, 'resource_link'].values
                if len(res_link) > 0 and pd.notnull(res_link[0]) and res_link[0].strip() != "":
                    st.markdown(f"🔗 **Reference Material:** [Open Resource Link]({res_link[0]})")
                
                with conn.cursor() as cursor_sync:
                    class_students = pd.read_sql_query(f"SELECT student_id FROM Students WHERE class_level = '{sel_cls}'", conn)
                    for _, st_row in class_students.iterrows():
                        cursor_sync.execute('''
                            INSERT INTO Assignment_Submissions (assignment_id, student_id, status, remarks)
                            VALUES (%s, %s, 'Pending', '')
                            ON CONFLICT (assignment_id, student_id) DO NOTHING;
                        ''', (asg_id, int(st_row['student_id'])))
                conn.commit()
                
                sub_df = pd.read_sql_query(f'''
                    SELECT sub.submission_id, s.student_id, s.first_name || ' ' || s.last_name AS Student_Name, sub.status, sub.remarks 
                    FROM Students s
                    LEFT JOIN Assignment_Submissions sub ON s.student_id = sub.student_id AND sub.assignment_id = {asg_id}
                    WHERE s.class_level = '{sel_cls}'
                ''', conn)
                
                if sub_df.empty:
                    st.info("No students enrolled in this class.")
                else:
                    completed_count = len(sub_df[sub_df['status'] == "Completed"])
                    total_count = len(sub_df)
                    prog_val = (completed_count / total_count) if total_count > 0 else 0.0
                    st.markdown(f"**Batch Completion Progress:** {completed_count}/{total_count} Students Completed")
                    st.progress(prog_val)
                    st.markdown("<br>", unsafe_allow_html=True)
                    
                    st.markdown(f"#### 📝 Submissions & Remarks for: {selected_asg_label}")
                    with st.form("asg_tracking_form"):
                        updated_rows = []
                        with conn.cursor() as cursor_sync:
                            for _, row in sub_df.iterrows():
                                sub_id = row['submission_id']
                                if pd.isna(sub_id):
                                    cursor_sync.execute('''
                                        INSERT INTO Assignment_Submissions (assignment_id, student_id, status, remarks)
                                        VALUES (%s, %s, 'Pending', '') RETURNING submission_id
                                    ''', (asg_id, int(row['student_id'])))
                                    conn.commit()
                                    sub_id = cursor_sync.fetchone()[0]
                                
                                c1, c2, c3 = st.columns([2, 1, 2])
                                name_val = row['student_name'] if 'student_name' in row else row['Student_Name']
                                c1.markdown(f"**{name_val}**")
                                is_completed = c2.checkbox("Completed", value=(row['status'] == "Completed"), key=f"chk_{asg_id}_{row['student_id']}")
                                current_remark = str(row['remarks']) if pd.notnull(row['remarks']) else ""
                                remark_val = c3.text_input("Remarks", value=current_remark, key=f"rem_{asg_id}_{row['student_id']}", label_visibility="collapsed")
                                
                                updated_rows.append((int(sub_id), "Completed" if is_completed else "Pending", remark_val))
                        
                        if st.form_submit_button("💾 Save Submissions & Remarks", use_container_width=True):
                            with conn.cursor() as cursor:
                                for s_id, stat, rem in updated_rows:
                                    cursor.execute("UPDATE Assignment_Submissions SET status = %s, remarks = %s WHERE submission_id = %s", (stat, rem, s_id))
                            conn.commit()
                            st.toast("Assignment progress saved successfully!", icon="🎉")
                            st.rerun()
        else:
            asgs = pd.read_sql_query(f"SELECT assignment_id, subject, title, due_date FROM Assignments WHERE class_level = '{sel_cls}'", conn)
            if asgs.empty:
                st.info("No assignments found for this class.")
            else:
                asg_opts = {f"[{r['subject']}] {r['title']} (Due: {r['due_date']})": r['assignment_id'] for _, r in asgs.iterrows()}
                selected_del_label = st.selectbox("Select Assignment to Permanently Delete", list(asg_opts.keys()), key="del_asg_sel")
                del_asg_id = int(asg_opts[selected_del_label])
                
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("⚠️ Permanently Delete Assignment", use_container_width=True):
                    with conn.cursor() as cursor:
                        cursor.execute("DELETE FROM Assignment_Submissions WHERE assignment_id = %s", (del_asg_id,))
                        cursor.execute("DELETE FROM Assignments WHERE assignment_id = %s", (del_asg_id,))
                    conn.commit()
                    st.toast("Assignment deleted permanently.", icon="🗑️")
                    st.rerun()

# --- AUTOMATED WHATSAPP BROADCASTS ---
elif choice == "📢 Broadcasts":
    st.subheader("📢 Automated WhatsApp Parent Broadcast Hub")
    b_class = st.selectbox("Target Class Broadcast", CLASS_LEVELS, key="bc_cls")
    
    with get_connection() as conn:
        target_condition = st.selectbox("Target Audience Filter", ["All Parents in Class", "Debarred Students Only (<75% Attendance)"])
        
        if target_condition == "All Parents in Class":
            students_bc = pd.read_sql_query(f"SELECT first_name, last_name, parent_phone FROM Students WHERE class_level = '{b_class}'", conn)
        else:
            all_st = pd.read_sql_query(f"SELECT student_id, first_name, last_name, parent_phone FROM Students WHERE class_level = '{b_class}'", conn)
            deb_ids = []
            for _, st_row in all_st.iterrows():
                t = pd.read_sql_query(f"SELECT COUNT(*) as cnt FROM Attendance WHERE student_id = {st_row['student_id']}", conn).iloc[0]['cnt']
                p = pd.read_sql_query(f"SELECT COUNT(*) as cnt FROM Attendance WHERE student_id = {st_row['student_id']} AND status = 'Present'", conn).iloc[0]['cnt']
                rate = (p / t * 100) if t > 0 else 100.0
                if rate < 75.0:
                    deb_ids.append(st_row['student_id'])
            students_bc = all_st[all_st['student_id'].isin(deb_ids)] if deb_ids else pd.DataFrame(columns=['first_name', 'last_name', 'parent_phone'])
        
        if students_bc.empty:
            st.warning("No parent contacts match the selected broadcast filter.")
        else:
            st.markdown(f"**Target Audience:** Class {b_class} ({len(students_bc)} Parents)")
            st.markdown("💡 *Tip: You can use `{student_name}` inside your message template to dynamically insert the student's name.*")
            msg_template = st.text_area("Broadcast Message Template", value="Dear Parent, this is an important administrative update regarding {student_name} at BLJ Classes.")
            
            if st.button("Generate Broadcast Links", use_container_width=True):
                st.markdown("### Click below to transmit via WhatsApp Web/App:")
                for _, row in students_bc.iterrows():
                    student_full_name = f"{row['first_name']} {row['last_name']}"
                    personalized_msg = msg_template.replace("{student_name}", student_full_name)
                    wa_url = f"https://wa.me/{row['parent_phone']}?text={urllib.parse.quote(personalized_msg)}"
                    st.markdown(f"- **{student_full_name}** ({row['parent_phone']}): [💬 Open WhatsApp Chat]({wa_url})", unsafe_allow_html=True)

# --- 5. REPORT CARDS ---
elif choice == "🖨️ Report Cards":
    st.subheader("Institutional Transcript Generator")
    with get_connection() as conn:
        s_df = pd.read_sql_query("SELECT student_id, first_name, last_name FROM Students", conn)
        student_opts = [f"{r['student_id']} - {r['first_name']} {r['last_name']}" for _, r in s_df.iterrows()]
        sel_stud = st.selectbox("Select Student", student_opts)
        
        if st.button("🖨️ Generate PDF Transcript", use_container_width=True):
            sid = int(sel_stud.split(" - ")[0])
            res = pd.read_sql_query(f"SELECT te.exam_type, tr.marks_obtained, te.max_marks FROM Test_Results tr JOIN Tests_Exams te ON tr.test_id = te.test_id WHERE tr.student_id = {sid}", conn).values.tolist()
            if not res:
                st.error("No data found.")
            else:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT first_name, last_name FROM Students WHERE student_id = %s", (sid,))
                    s_data = cursor.fetchone()
                
                fig, ax = plt.subplots(figsize=(6, 4))
                ax.bar([r[0] for r in res], [(r[1]/r[2])*100 for r in res], color='#0f172a', width=0.4)
                ax.set_ylim(0, 100)
                fig.savefig('chart.png', bbox_inches='tight')
                plt.close(fig)

                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", 'B', 16)
                pdf.cell(200, 10, txt=f"Transcript: {s_data[0]} {s_data[1]}", ln=True, align='C')
                pdf.image('chart.png', x=40, y=45, w=130)
                pdf.output(f"{s_data[0]}_Report.pdf")
                os.remove('chart.png')
                
                with open(f"{s_data[0]}_Report.pdf", "rb") as f:
                    st.download_button("⬇️ Download PDF Transcript", data=f, file_name=f"{s_data[0]}_Transcript.pdf", mime="application/pdf", use_container_width=True)
                st.toast("Transcript compiled successfully.", icon="🎉")

# --- 6. CLASS OVERVIEW ---
elif choice == "📊 Class Overview":
    st.subheader("📊 Institutional Analytics Dashboard")
    selected_class = st.selectbox("Class Tier", CLASS_LEVELS, key="ov_cls")
    with get_connection() as conn:
        q = f'''
            SELECT s.first_name || ' ' || s.last_name AS Student_Name, sub.subject_name AS Subject, te.exam_type AS Exam, tr.marks_obtained AS Marks, te.max_marks AS Max, ROUND(((tr.marks_obtained * 100.0) / te.max_marks)::numeric, 2) AS Percentage
            FROM Test_Results tr JOIN Students s ON tr.student_id = s.student_id JOIN Tests_Exams te ON tr.test_id = te.test_id JOIN Subjects sub ON te.subject_id = sub.subject_id WHERE s.class_level = '{selected_class}'
        '''
        res_df = pd.read_sql_query(q, conn)
        if res_df.empty:
            st.info("No analytics data available.")
        else:
            st.dataframe(res_df, hide_index=True, use_container_width=True)
            st.download_button("⬇️ Export Master CSV", data=res_df.to_csv(index=False).encode('utf-8'), file_name=f"Class_{selected_class}_Master.csv", mime="text/csv", use_container_width=True)
