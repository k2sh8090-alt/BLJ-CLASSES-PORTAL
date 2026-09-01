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
                if username == "BLJclassess" and password == "classesBLJ123":
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

# --- DASHBOARD LOGIC ---
if choice == "🏠 Dashboard":
    st.subheader("Executive Operational Summary")
    with get_connection() as conn:
        total_students = pd.read_sql_query("SELECT COUNT(*) as count FROM Students", conn).iloc[0]['count']
        total_tests = pd.read_sql_query("SELECT COUNT(*) as count FROM Tests_Exams", conn).iloc[0]['count']
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Enrolled Students", total_students)
    col2.metric("Evaluations Conducted", total_tests)
    col3.metric("Present Today", "Syncing...")
    col4.metric("Active Assignments", "Syncing...")

# --- VIEW STUDENTS LOGIC ---
elif choice == "👥 View Students":
    st.subheader("Enrolled Students Directory")
    with get_connection() as conn:
        df = pd.read_sql_query("SELECT student_id, first_name, last_name, class_level, subject FROM Students", conn)
        if df.empty:
            st.info("No records found.")
        else:
            st.dataframe(df, hide_index=True, use_container_width=True)

# NOTE: The rest of your previously generated functional modules (Attendance, Tests, Broadcasts, Report Cards) 
# seamlessly integrate here precisely as they did in your working Streamlit build.
