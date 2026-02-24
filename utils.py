import streamlit as st
import pandas as pd
import os
from datetime import date
import auth  # our new auth module

FILES = {
    "students":          "students.csv",
    "teachers":          "teachers.csv",
    "student_attendance":"student_attendance.csv",
    "teacher_attendance":"teacher_attendance.csv",
    "results":           "results.csv",
}

# ─────────────────────────────────────────────────────────────────────────────
# 1. THEME & STYLING
# ─────────────────────────────────────────────────────────────────────────────
def apply_styling():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

        html, body, [class*="css"] {
            font-family: 'Poppins', sans-serif;
        }

        /* ── App Background ── */
        .stApp { background-color: #FDFBF7; }

        /* ── Sidebar ── */
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #1a1a2e 0%, #16213e 60%, #0f3460 100%);
            border-right: none;
        }
        section[data-testid="stSidebar"] * { color: #e0e0e0 !important; }
        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3 { color: #ffffff !important; }
        section[data-testid="stSidebar"] .stCaption { color: #a0a0c0 !important; }

        section[data-testid="stSidebar"] .stButton button {
            width: 100%;
            border-radius: 10px;
            border: 1px solid transparent;
            background-color: rgba(255,255,255,0.05);
            color: #d0d0e8 !important;
            text-align: left;
            padding: 0.5rem 1rem;
            transition: all 0.25s ease;
            font-size: 0.9rem;
        }
        section[data-testid="stSidebar"] .stButton button:hover {
            background-color: rgba(230,126,34,0.25);
            border: 1px solid rgba(230,126,34,0.5);
            color: #ffffff !important;
            transform: translateX(4px);
        }

        /* ── Headers ── */
        h1, h2, h3 { color: #2C3E50; font-weight: 600; }

        /* ── Metric Cards ── */
        [data-testid="stMetricValue"] { font-size: 2.5rem; color: #E67E22; }

        /* ── Input Fields ── */
        .stTextInput > div > div > input,
        .stSelectbox > div > div,
        .stNumberInput > div > div > input {
            border-radius: 8px;
            border: 1px solid #EAE0C8;
        }

        /* ── Status Badges ── */
        .status-present { background:#d4edda; color:#155724; padding:4px 10px; border-radius:20px; font-weight:600; font-size:0.85rem; }
        .status-absent  { background:#f8d7da; color:#721c24; padding:4px 10px; border-radius:20px; font-weight:600; font-size:0.85rem; }
        .status-leave   { background:#fff3cd; color:#856404; padding:4px 10px; border-radius:20px; font-weight:600; font-size:0.85rem; }

        /* ── Buttons ── */
        div.stButton > button:first-child {
            border-radius: 8px;
            font-weight: 500;
            transition: all 0.2s ease;
        }

        /* ── Role Badge ── */
        .role-badge {
            display: inline-block;
            padding: 3px 12px;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: 600;
            margin-left: 6px;
        }
        .role-admin     { background: #4a0e8f; color: #fff; }
        .role-principal { background: #0f3460; color: #fff; }
        .role-teacher   { background: #1a6b3c; color: #fff; }

        /* ── Login Page ── */
        .login-card {
            background: #fff;
            border-radius: 20px;
            padding: 2.5rem 3rem;
            box-shadow: 0 20px 60px rgba(0,0,0,0.12);
            max-width: 440px;
            margin: 3rem auto;
        }
        .login-logo {
            text-align: center;
            font-size: 3.5rem;
            margin-bottom: 0.5rem;
        }
        .login-title {
            text-align: center;
            font-size: 1.5rem;
            font-weight: 700;
            color: #1a1a2e;
            margin-bottom: 0.2rem;
        }
        .login-sub {
            text-align: center;
            font-size: 0.85rem;
            color: #888;
            margin-bottom: 1.8rem;
        }
        </style>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# 2. LOGIN PAGE
# ─────────────────────────────────────────────────────────────────────────────
def page_login():
    """Renders the login form. On success calls auth.login()."""
    # Centre the card
    _, mid, _ = st.columns([1, 2, 1])
    with mid:
        st.markdown("""
            <div class="login-logo">🏫</div>
            <div class="login-title">Sun Shine School</div>
            <div class="login-sub">Management System &nbsp;·&nbsp; Please sign in</div>
        """, unsafe_allow_html=True)

        with st.form("login_form"):
            username = st.text_input("👤 Username", placeholder="Enter your username")
            password = st.text_input("🔒 Password", type="password", placeholder="Enter your password")
            submitted = st.form_submit_button("Sign In →", use_container_width=True)

        if submitted:
            if not username or not password:
                st.error("Please enter both username and password.")
            else:
                user = auth.authenticate(username, password)
                if user:
                    auth.login(user)
                    st.rerun()
                else:
                    st.error("❌ Invalid username or password.")

        # Hint box
        st.markdown("---")
        st.caption("**Default credentials for demo:**")
        st.caption("Admin → `admin` / `admin123`")
        st.caption("Principal → `principal` / `principal123`")
        st.caption("Teacher → `teacher` / `teacher123`")


# ─────────────────────────────────────────────────────────────────────────────
# 3. STATE INITIALIZATION & PERSISTENCE
# ─────────────────────────────────────────────────────────────────────────────
def load_data():
    """Load data from CSV files or create empty DataFrames if files don't exist."""
    # Students
    if os.path.exists(FILES["students"]):
        st.session_state.students = pd.read_csv(FILES["students"])
        st.session_state.students["Class"] = st.session_state.students["Class"].astype(str)
    elif "students" not in st.session_state:
        st.session_state.students = pd.DataFrame(columns=["Student ID", "Name", "Class"])

    # Teachers
    if os.path.exists(FILES["teachers"]):
        st.session_state.teachers = pd.read_csv(FILES["teachers"])
    elif "teachers" not in st.session_state:
        st.session_state.teachers = pd.DataFrame(columns=["Teacher ID", "Name", "Subject", "Phone"])

    # Student Attendance
    if os.path.exists(FILES["student_attendance"]):
        st.session_state.student_attendance = pd.read_csv(FILES["student_attendance"])
        st.session_state.student_attendance["Class"] = st.session_state.student_attendance["Class"].astype(str)
    elif "student_attendance" not in st.session_state:
        st.session_state.student_attendance = pd.DataFrame(columns=["Student ID", "Name", "Class", "Date", "Status"])

    # Teacher Attendance
    if os.path.exists(FILES["teacher_attendance"]):
        st.session_state.teacher_attendance = pd.read_csv(FILES["teacher_attendance"])
    elif "teacher_attendance" not in st.session_state:
        st.session_state.teacher_attendance = pd.DataFrame(columns=["Teacher ID", "Name", "Date", "Status"])

    # Results
    if os.path.exists(FILES["results"]):
        st.session_state.results = pd.read_csv(FILES["results"])
    elif "results" not in st.session_state:
        st.session_state.results = pd.DataFrame(columns=["Student ID", "Name", "Subject", "Marks", "Grade"])

    if "current_page" not in st.session_state:
        st.session_state.current_page = "Dashboard"


def save_data(key):
    """Save the specific dataframe to CSV."""
    if key in st.session_state and key in FILES:
        st.session_state[key].to_csv(FILES[key], index=False)


# ─────────────────────────────────────────────────────────────────────────────
# 4. SIDEBAR NAVIGATION (role-filtered)
# ─────────────────────────────────────────────────────────────────────────────
def sidebar_navigation():
    user      = auth.get_current_user()
    role      = user.get("role", "")
    name      = user.get("name", "User")
    allowed   = auth.get_allowed_pages()

    role_colors = {"admin": "#7c3aed", "principal": "#0f3460", "teacher": "#1a6b3c"}
    role_color  = role_colors.get(role, "#555")

    with st.sidebar:
        st.markdown(f"""
            <div style='text-align:center; padding: 1rem 0 0.5rem 0;'>
                <div style='font-size:2.5rem'>🏫</div>
                <div style='font-size:1.1rem; font-weight:700; color:#fff; margin-top:4px;'>Sun Shine School</div>
                <div style='margin-top:6px;'>
                    <span style='background:{role_color}; color:#fff; padding:2px 12px;
                                 border-radius:20px; font-size:0.72rem; font-weight:600;
                                 text-transform:uppercase; letter-spacing:0.5px;'>{role}</span>
                </div>
                <div style='font-size:0.82rem; color:#bbb; margin-top:6px;'>{name}</div>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("---")

        # ── Navigation items ──
        if "Dashboard" in allowed:
            if st.button("🏠  Dashboard"):
                st.session_state.current_page = "Dashboard"

        # Management section (principal + admin only)
        if any(p in allowed for p in ["Add Student", "Add Teacher"]):
            st.caption("Management")
            if "Add Student" in allowed and st.button("👨‍🎓  Add Student"):
                st.session_state.current_page = "Add Student"
            if "Add Teacher" in allowed and st.button("👩‍🏫  Add Teacher"):
                st.session_state.current_page = "Add Teacher"

        # Academic section
        if any(p in allowed for p in ["Student Attendance", "Teacher Attendance", "Student Results"]):
            st.caption("Academic")
            if "Student Attendance" in allowed and st.button("📅  Student Attendance"):
                st.session_state.current_page = "Student Attendance"
            if "Teacher Attendance" in allowed and st.button("📋  Teacher Attendance"):
                st.session_state.current_page = "Teacher Attendance"
            if "Student Results" in allowed and st.button("📊  Student Results"):
                st.session_state.current_page = "Student Results"

        # Records
        if "View Records" in allowed:
            st.markdown("---")
            if st.button("📂  View Records"):
                st.session_state.current_page = "View Records"

        # Admin-only: Manage Users
        if "Manage Users" in allowed:
            if st.button("🔑  Manage Users"):
                st.session_state.current_page = "Manage Users"

        # Logout
        st.markdown("---")
        if st.button("🚪  Sign Out", use_container_width=True):
            auth.logout()

    return st.session_state.current_page


# ─────────────────────────────────────────────────────────────────────────────
# 5. PAGES
# ─────────────────────────────────────────────────────────────────────────────

# ── 5.1 Dashboard ─────────────────────────────────────────────────────────────
def page_dashboard():
    user = auth.get_current_user()
    role = user.get("role", "")
    name = user.get("name", "User")

    role_icons = {"admin": "🛡️", "principal": "🎓", "teacher": "📚"}
    icon = role_icons.get(role, "👋")

    st.title(f"🏫 Welcome, {name} {icon}")
    role_labels = {"admin": "System Administrator", "principal": "Principal", "teacher": "Teacher"}
    st.caption(f"Role: **{role_labels.get(role, role.title())}**  ·  Sun Shine School Management System")
    st.divider()

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Students", len(st.session_state.students))
    with col2:
        st.metric("Total Teachers", len(st.session_state.teachers))
    with col3:
        st.metric("Total Results", len(st.session_state.results))

    st.divider()
    st.subheader("Quick Actions")
    allowed = auth.get_allowed_pages()

    c1, c2, c3 = st.columns(3)
    if "Add Student" in allowed:
        with c1:
            st.info("👨‍🎓 Go to **Add Student** to enroll new students.")
    if "Student Attendance" in allowed:
        with c2:
            st.info("📅 Use **Student Attendance** to mark daily attendance.")
    if "Student Results" in allowed:
        with c3:
            st.info("📊 Check **Student Results** to manage exam scores.")


# ── 5.2 Add Student ───────────────────────────────────────────────────────────
def page_add_student():
    st.title("👨‍🎓 Add New Student")

    with st.form("add_student_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            sid  = st.text_input("Student ID", placeholder="e.g. S-101")
            name = st.text_input("Full Name",  placeholder="John Doe")
        with col2:
            cls = st.selectbox("Class", options=[str(x) for x in range(1, 11)])

        submitted = st.form_submit_button("➕ Submit Student", use_container_width=True)

        if submitted:
            if not sid or not name:
                st.warning("⚠️ Please fill in all required fields.")
            elif not st.session_state.students.empty and sid in st.session_state.students["Student ID"].values:
                st.error(f"❌ Student ID **{sid}** already exists!")
            else:
                new_data = pd.DataFrame([[sid, name, cls]], columns=["Student ID", "Name", "Class"])
                st.session_state.students = pd.concat([st.session_state.students, new_data], ignore_index=True)
                save_data("students")
                st.success(f"✅ Student **{name}** added successfully!")

    # Display
    st.divider()
    st.subheader("📋 All Students")
    if not st.session_state.students.empty:
        classes = sorted(st.session_state.students["Class"].unique().tolist(), key=lambda x: int(x) if x.isdigit() else x)
        filter_cls = st.selectbox("Filter by Class", ["All"] + classes, key="stu_filter")
        df_show = st.session_state.students
        if filter_cls != "All":
            df_show = df_show[df_show["Class"] == filter_cls]
        st.dataframe(df_show, use_container_width=True)
    else:
        st.info("No students added yet.")


# ── 5.3 Add Teacher ───────────────────────────────────────────────────────────
def page_add_teacher():
    st.title("👩‍🏫 Add New Teacher")
    with st.form("add_teacher_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            tid   = st.text_input("Teacher ID",   placeholder="e.g. T-501")
            tname = st.text_input("Full Name",     placeholder="Jane Smith")
        with col2:
            phone   = st.text_input("Phone Number")
            subject = st.selectbox("Subject", ["English", "Math", "Computer", "Urdu", "S.Study", "Science"])

        submitted = st.form_submit_button("➕ Submit Teacher", use_container_width=True)

        if submitted:
            if not tid or not tname or not phone:
                st.warning("⚠️ Please fill in all fields.")
            elif tid in st.session_state.teachers["Teacher ID"].values:
                st.error(f"❌ Teacher ID **{tid}** already exists!")
            else:
                new_data = pd.DataFrame([[tid, tname, subject, phone]], columns=st.session_state.teachers.columns)
                st.session_state.teachers = pd.concat([st.session_state.teachers, new_data], ignore_index=True)
                save_data("teachers")
                st.success(f"✅ Teacher **{tname}** added successfully!")


# ── 5.4 Student Attendance ────────────────────────────────────────────────────
def page_student_attendance():
    st.title("📅 Student Attendance")

    if st.session_state.students.empty:
        st.warning("⚠️ No students found. Please add students first.")
        return

    col1, col2 = st.columns(2)
    with col1:
        att_date = st.date_input("Select Date", date.today())
    with col2:
        classes = sorted(st.session_state.students["Class"].unique().tolist(), key=lambda x: int(x) if x.isdigit() else x)
        selected_class = st.selectbox("Select Class", classes)

    st.divider()
    st.subheader("📝 Mark Attendance")

    class_students = st.session_state.students[st.session_state.students["Class"] == selected_class]

    if class_students.empty:
        st.info("No students in this class.")
    else:
        student_name = st.selectbox("Select Student", class_students["Name"])

        c1, c2, c3 = st.columns(3)
        status = None
        if c1.button("✅ Present", use_container_width=True):
            status = "Present"
        if c2.button("❌ Absent",  use_container_width=True):
            status = "Absent"
        if c3.button("⚠️ Leave",   use_container_width=True):
            status = "Leave"

        if status:
            sid      = class_students[class_students["Name"] == student_name].iloc[0]["Student ID"]
            date_str = str(att_date)

            # Remove duplicate for same day
            st.session_state.student_attendance = st.session_state.student_attendance[
                ~((st.session_state.student_attendance["Student ID"] == sid) &
                  (st.session_state.student_attendance["Date"] == date_str))
            ]
            new_att = pd.DataFrame([{
                "Student ID": sid, "Name": student_name,
                "Class": selected_class, "Date": date_str, "Status": status
            }])
            st.session_state.student_attendance = pd.concat([st.session_state.student_attendance, new_att], ignore_index=True)
            save_data("student_attendance")
            st.success(f"Marked **{student_name}** as **{status}**")
            st.rerun()

    # History
    st.divider()
    st.subheader("📊 Attendance History")
    view_df = st.session_state.student_attendance
    view_df = view_df[view_df["Class"] == selected_class]
    view_df = view_df[view_df["Date"] == str(att_date)]
    if not view_df.empty:
        st.dataframe(view_df.reset_index(drop=True), use_container_width=True)
    else:
        st.info(f"No records for Class {selected_class} on {att_date}.")


# ── 5.5 Teacher Attendance ────────────────────────────────────────────────────
def page_teacher_attendance():
    st.title("📋 Teacher Attendance")

    if st.session_state.teachers.empty:
        st.warning("⚠️ No teachers found. Please add teachers first.")
        return

    att_date = st.date_input("Select Date", date.today())
    st.divider()
    st.subheader("📝 Mark Attendance")

    teacher_name = st.selectbox("Select Teacher", st.session_state.teachers["Name"])

    c1, c2, c3 = st.columns(3)
    status = None
    if c1.button("✅ Present", key="t_pres",  use_container_width=True): status = "Present"
    if c2.button("❌ Absent",  key="t_abs",   use_container_width=True): status = "Absent"
    if c3.button("⚠️ Leave",   key="t_leave", use_container_width=True): status = "Leave"

    if status:
        tid      = st.session_state.teachers[st.session_state.teachers["Name"] == teacher_name].iloc[0]["Teacher ID"]
        date_str = str(att_date)

        st.session_state.teacher_attendance = st.session_state.teacher_attendance[
            ~((st.session_state.teacher_attendance["Teacher ID"] == tid) &
              (st.session_state.teacher_attendance["Date"] == date_str))
        ]
        new_att = pd.DataFrame([{"Teacher ID": tid, "Name": teacher_name, "Date": date_str, "Status": status}])
        st.session_state.teacher_attendance = pd.concat([st.session_state.teacher_attendance, new_att], ignore_index=True)
        save_data("teacher_attendance")
        st.success(f"Marked **{teacher_name}** as **{status}**")
        st.rerun()

    st.divider()
    st.subheader("📊 Attendance History")
    view_df = st.session_state.teacher_attendance
    view_df = view_df[view_df["Date"] == str(att_date)]
    if not view_df.empty:
        st.dataframe(view_df.reset_index(drop=True), use_container_width=True)
    else:
        st.info(f"No teacher records for {att_date}.")


# ── 5.6 Student Results ───────────────────────────────────────────────────────
def page_student_results():
    st.title("📊 Student Results")

    if st.session_state.students.empty:
        st.warning("⚠️ No students found.")
        return

    col1, col2 = st.columns(2)
    with col1:
        classes = sorted(st.session_state.students["Class"].unique().tolist(), key=lambda x: int(x) if x.isdigit() else x)
        selected_class = st.selectbox("Select Class", classes)

    class_students = st.session_state.students[st.session_state.students["Class"] == selected_class]
    if class_students.empty:
        st.info("No students in this class.")
        return

    with col2:
        student_name = st.selectbox("Select Student", class_students["Name"])

    st.divider()
    st.subheader("📝 Add / Update Result")

    with st.form("result_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            subject = st.selectbox("Subject", ["English", "Math", "Computer", "Urdu", "S.Study", "Science", "Islamiyat"])
        with c2:
            marks = st.number_input("Marks Obtained", min_value=0, max_value=100, step=1)

        submitted = st.form_submit_button("💾 Save Result", use_container_width=True)

        if submitted:
            grade = (
                "A+" if marks >= 90 else "A" if marks >= 80 else
                "B"  if marks >= 70 else "C" if marks >= 60 else
                "D"  if marks >= 50 else "F"
            )
            sid = class_students[class_students["Name"] == student_name].iloc[0]["Student ID"]

            # Remove old entry for same student+subject (update behaviour)
            st.session_state.results = st.session_state.results[
                ~((st.session_state.results["Name"] == student_name) &
                  (st.session_state.results["Subject"] == subject))
            ]
            new_res = pd.DataFrame([{
                "Student ID": sid, "Name": student_name,
                "Subject": subject, "Marks": marks, "Grade": grade
            }])
            st.session_state.results = pd.concat([st.session_state.results, new_res], ignore_index=True)
            save_data("results")
            st.success(f"✅ Saved: {subject} — {marks} ({grade})")
            st.rerun()

    # View report card
    st.divider()
    st.subheader(f"📜 Report Card: {student_name}")
    student_results = st.session_state.results[st.session_state.results["Name"] == student_name]
    if not student_results.empty:
        display_df = student_results[["Subject", "Marks", "Grade"]].reset_index(drop=True)
        st.dataframe(display_df, use_container_width=True, hide_index=True)
        avg_marks = student_results["Marks"].mean()
        st.caption(f"**Average Marks:** {avg_marks:.2f}")
    else:
        st.info("No results for this student yet.")


# ── 5.7 View Records ──────────────────────────────────────────────────────────
def page_view_records():
    st.title("📂 System Records")
    tab1, tab2, tab3, tab4 = st.tabs(["👨‍🎓 Students", "👩‍🏫 Teachers", "📅 Attendance", "📊 Results"])

    with tab1:
        if not st.session_state.students.empty:
            classes    = sorted(st.session_state.students["Class"].unique().tolist(), key=lambda x: int(x) if x.isdigit() else x)
            cls_filter = st.selectbox("Filter by Class", ["All"] + classes)
            df = st.session_state.students
            if cls_filter != "All":
                df = df[df["Class"] == cls_filter]
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No students registered.")

    with tab2:
        st.dataframe(st.session_state.teachers, use_container_width=True)

    with tab3:
        st.subheader("Student Attendance")
        st.dataframe(st.session_state.student_attendance, use_container_width=True)
        st.divider()
        st.subheader("Teacher Attendance")
        st.dataframe(st.session_state.teacher_attendance, use_container_width=True)

    with tab4:
        st.dataframe(st.session_state.results, use_container_width=True)


# ── 5.8 Manage Users (Admin only) ─────────────────────────────────────────────
def page_manage_users():
    st.title("🔑 Manage Users")
    st.caption("Add, update or remove system accounts. Changes take effect immediately.")

    users_df = auth.load_users()

    # ── Current Users Table ──
    st.subheader("👥 Current Users")
    display = users_df[["username", "name", "role"]].copy()
    display.columns = ["Username", "Name", "Role"]
    st.dataframe(display, use_container_width=True, hide_index=True)

    st.divider()

    # ── Add New User ──
    st.subheader("➕ Add New User")
    with st.form("add_user_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            new_username = st.text_input("Username", placeholder="e.g. teacher2")
            new_name     = st.text_input("Full Name", placeholder="e.g. Mr. Ali")
        with c2:
            new_password = st.text_input("Password", type="password", placeholder="Set a password")
            new_role     = st.selectbox("Role", ["teacher", "principal", "admin"])

        add_submitted = st.form_submit_button("➕ Add User", use_container_width=True)

        if add_submitted:
            if not new_username or not new_name or not new_password:
                st.warning("⚠️ Please fill in all fields.")
            elif new_username.lower() in users_df["username"].str.lower().values:
                st.error(f"❌ Username **{new_username}** already exists!")
            else:
                new_row = pd.DataFrame([{
                    "username": new_username,
                    "password": new_password,
                    "role":     new_role,
                    "name":     new_name
                }])
                users_df = pd.concat([users_df, new_row], ignore_index=True)
                auth.save_users(users_df)
                st.success(f"✅ User **{new_name}** ({new_role}) added!")
                st.rerun()

    st.divider()

    # ── Change Password ──
    st.subheader("🔒 Change Password")
    with st.form("change_pw_form", clear_on_submit=True):
        target_user = st.selectbox("Select User", users_df["username"].tolist())
        new_pw      = st.text_input("New Password", type="password")
        pw_submit   = st.form_submit_button("Update Password", use_container_width=True)

        if pw_submit:
            if not new_pw:
                st.warning("⚠️ Password cannot be empty.")
            else:
                users_df.loc[users_df["username"] == target_user, "password"] = new_pw
                auth.save_users(users_df)
                st.success(f"✅ Password updated for **{target_user}**.")
                st.rerun()

    st.divider()

    # ── Delete User ──
    st.subheader("🗑️ Remove User")
    deletable = [u for u in users_df["username"].tolist() if u != auth.get_current_user().get("username")]
    if deletable:
        with st.form("delete_user_form", clear_on_submit=True):
            del_user   = st.selectbox("Select User to Remove", deletable)
            del_submit = st.form_submit_button("🗑️ Delete User", use_container_width=True)

            if del_submit:
                users_df = users_df[users_df["username"] != del_user]
                auth.save_users(users_df)
                st.success(f"✅ User **{del_user}** removed.")
                st.rerun()
    else:
        st.info("No other users to delete.")
