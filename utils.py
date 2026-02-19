import streamlit as st
import pandas as pd
import os
import random
from datetime import date

FILES = {
    "students": "students.csv",
    "teachers": "teachers.csv",
    "student_attendance": "student_attendance.csv",
    "teacher_attendance": "teacher_attendance.csv",
    "results": "results.csv"
}

# -----------------------------------------------------------------------------
# 1. THEME & STYLING
# -----------------------------------------------------------------------------
def apply_styling():
    st.markdown("""
        <style>
        /* Import Google Font */
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');

        html, body, [class*="css"] {
            font-family: 'Poppins', sans-serif;
        }

        /* Essential Backgrounds */
        .stApp {
            background-color: #FDFBF7; /* Warm White */
        }
        section[data-testid="stSidebar"] {
            background-color: #F5E6CA; /* Soft Gold/Beige */
            border-right: 1px solid #EAE0C8;
        }

        /* Customizing sidebar buttons to look like links */
        section[data-testid="stSidebar"] .stButton button {
            width: 100%;
            border-radius: 8px;
            border: 1px solid transparent;
            background-color: transparent;
            color: #4A4A4A;
            text-align: left;
            padding: 0.5rem 1rem;
            transition: all 0.3s ease;
        }

        section[data-testid="stSidebar"] .stButton button:hover {
            background-color: #FFFFFF;
            border: 1px solid #EAE0C8;
            color: #000;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
            transform: translateX(5px);
        }

        /* Headers */
        h1, h2, h3 {
            color: #2C3E50;
            font-weight: 600;
        }
        
        /* Metric Cards */
        [data-testid="stMetricValue"] {
            font-size: 2.5rem;
            color: #E67E22; /* Accent Color */
        }
        
        /* Input Fields */
        .stTextInput > div > div > input {
            border-radius: 8px;
            border: 1px solid #EAE0C8;
        }

        /* Status Badges */
        .status-present {
            background-color: #d4edda;
            color: #155724;
            padding: 4px 8px;
            border-radius: 4px;
            font-weight: bold;
        }
        .status-absent {
            background-color: #f8d7da;
            color: #721c24;
            padding: 4px 8px;
            border-radius: 4px;
            font-weight: bold;
        }
        .status-leave {
            background-color: #fff3cd;
            color: #856404;
            padding: 4px 8px;
            border-radius: 4px;
            font-weight: bold;
        }

        /* Button Enhancements */
        div.stButton > button:first-child {
            border-radius: 8px;
            font-weight: 500;
        }
        
        </style>
    """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. STATE INITIALIZATION & PERSISTENCE
# -----------------------------------------------------------------------------
def load_data():
    """Load data from CSV files or create empty DataFrames if files don't exist."""
    
    # 1. Students
    if os.path.exists(FILES["students"]):
        st.session_state.students = pd.read_csv(FILES["students"])
        # Ensure Class is string for consistent sorting/filtering
        st.session_state.students["Class"] = st.session_state.students["Class"].astype(str)
    elif "students" not in st.session_state:
        st.session_state.students = pd.DataFrame(columns=["Student ID", "Name", "Class"])

    # 2. Teachers
    if os.path.exists(FILES["teachers"]):
        st.session_state.teachers = pd.read_csv(FILES["teachers"])
    elif "teachers" not in st.session_state:
        st.session_state.teachers = pd.DataFrame(columns=["Teacher ID", "Name", "Subject", "Phone"])

    # 3. Student Attendance
    if os.path.exists(FILES["student_attendance"]):
        st.session_state.student_attendance = pd.read_csv(FILES["student_attendance"])
        st.session_state.student_attendance["Class"] = st.session_state.student_attendance["Class"].astype(str)
    elif "student_attendance" not in st.session_state:
        st.session_state.student_attendance = pd.DataFrame(columns=["Student ID", "Name", "Class", "Date", "Status"])

    # 4. Teacher Attendance
    if os.path.exists(FILES["teacher_attendance"]):
        st.session_state.teacher_attendance = pd.read_csv(FILES["teacher_attendance"])
    elif "teacher_attendance" not in st.session_state:
        st.session_state.teacher_attendance = pd.DataFrame(columns=["Teacher ID", "Name", "Date", "Status"])

    # 5. Results
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



# -----------------------------------------------------------------------------
# 3. SIDEBAR NAVIGATION
# -----------------------------------------------------------------------------
def sidebar_navigation():
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/201/201614.png", width=50) # Placeholder Icon
        st.title("Sun Shine School")
        st.markdown("---")
        
        # Navigation Buttons
        if st.button("🏠 Dashboard"):
            st.session_state.current_page = "Dashboard"
        
        st.caption("Management")
        if st.button("👨‍🎓 Add Student"):
            st.session_state.current_page = "Add Student"
        if st.button("👩‍🏫 Add Teacher"):
            st.session_state.current_page = "Add Teacher"
            
        st.caption("Academic")
        if st.button("📅 Student Attendance"):
            st.session_state.current_page = "Student Attendance"
        if st.button("📋 Teacher Attendance"):
            st.session_state.current_page = "Teacher Attendance"
        if st.button("📊 Student Results"):
            st.session_state.current_page = "Student Results"
            
        st.markdown("---")
        if st.button("📂 View Records"):
            st.session_state.current_page = "View Records"
            


    return st.session_state.current_page

# -----------------------------------------------------------------------------
# 4. PAGES
# -----------------------------------------------------------------------------

def page_dashboard():
    st.title("🏫 Dashboard Overview")
    st.markdown("Welcome to the **Sun Shine School Management System**. Here is a quick overview of the current stats.")
    st.divider()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Students", len(st.session_state.students))
    with col2:
        st.metric("Total Teachers", len(st.session_state.teachers))
    with col3:
        st.metric("Total Results", len(st.session_state.results))
    
    # Placeholder Chart (Optional - adds 'wow' factor)
    st.divider()
    st.subheader("Quick Actions")
    c1, c2 = st.columns(2)
    with c1:
        st.info("Navigate to 'Add Student' to enroll new students.")
    with c2:
        st.info("check 'View Records' to download reports.")

def page_add_student():
    st.title("👨‍🎓 Add New Student")
    
    # --- Add Student Form ---
    with st.form("add_student_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            sid = st.text_input("Student ID", placeholder="e.g. S-101")
            name = st.text_input("Full Name", placeholder="John Doe")
        with col2:
            cls = st.selectbox("Class", options=[str(x) for x in range(1, 11)])
            # Removed Reputation Score as requested
        
        submitted = st.form_submit_button("Submit Student Details")
        
        if submitted:
            if not sid or not name:
                st.warning("⚠️ Please fill in all required fields.")
            elif not st.session_state.students.empty and sid in st.session_state.students["Student ID"].values:
                st.error(f"❌ Student ID {sid} already exists!")
            else:
                new_data = pd.DataFrame([[sid, name, cls]], columns=["Student ID", "Name", "Class"])
                st.session_state.students = pd.concat([st.session_state.students, new_data], ignore_index=True)
                save_data("students") # Save to csv
                st.success(f"✅ Student **{name}** added successfully!")

    # --- Display All Students ---
    st.divider()
    st.subheader("📋 All Students List")
    
    if not st.session_state.students.empty:
        # Filter for the table
        classes = sorted(st.session_state.students["Class"].unique().tolist(), key=lambda x: int(x) if x.isdigit() else x)
        filter_cls = st.selectbox("Filter by Class", ["All"] + classes, key="stu_filter")
        
        df_show = st.session_state.students
        if filter_cls != "All":
            df_show = df_show[df_show["Class"] == filter_cls]
            
        try:
            st.dataframe(df_show, args={"width": "stretch"}) # Attempt to use new syntax if supported
        except:
             st.dataframe(df_show, use_container_width=True) # Fallback
    else:
        st.info("No students added yet.")

def page_add_teacher():
    st.title("👩‍🏫 Add New Teacher")
    with st.form("add_teacher_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            tid = st.text_input("Teacher ID", placeholder="e.g. T-501")
            name = st.text_input("Full Name", placeholder="Jane Smith")
        with col2:
            phone = st.text_input("Phone Number")
            subject = st.selectbox("Subject", options=["English", "Math", "Computer", "Urdu", "S.Study", "Science"])
        
        submitted = st.form_submit_button("Submit Teacher Details")
        
        if submitted:
            if not tid or not name or not phone:
                st.warning("⚠️ Please fill in all fields.")
            elif tid in st.session_state.teachers["Teacher ID"].values:
                st.error(f"❌ Teacher ID {tid} already exists!")
            else:
                new_data = pd.DataFrame([[tid, name, subject, phone]], columns=st.session_state.teachers.columns)
                st.session_state.teachers = pd.concat([st.session_state.teachers, new_data], ignore_index=True)
                save_data("teachers")
                st.success(f"✅ Teacher **{name}** added successfully!")

def page_student_attendance():
    st.title("📅 Student Attendance")
    
    if st.session_state.students.empty:
        st.warning("⚠️ No students found. Please add students first.")
        return

    # --- Filters ---
    col1, col2 = st.columns(2)
    with col1:
        att_date = st.date_input("Select Date", date.today())
    with col2:
        classes = sorted(st.session_state.students["Class"].unique().tolist(), key=lambda x: int(x) if x.isdigit() else x)
        selected_class = st.selectbox("Select Class", classes)
    
    # --- Mark Attendance Section ---
    st.divider()
    st.subheader("📝 Mark Attendance")
    
    class_students = st.session_state.students[st.session_state.students["Class"] == selected_class]
    
    if class_students.empty:
        st.info("No students in this class.")
    else:
        student_name = st.selectbox("Select Student", class_students["Name"])
        
        # Status Buttons
        c1, c2, c3 = st.columns(3)
        status = None
        
        # Use simple buttons for quick status toggle
        if c1.button("✅ Present", use_container_width=True):
            status = "Present"
        if c2.button("❌ Absent", use_container_width=True):
            status = "Absent"
        if c3.button("⚠️ Leave", use_container_width=True):
            status = "Leave"
            
        if status:
            sid = class_students[class_students["Name"] == student_name].iloc[0]["Student ID"]
            date_str = str(att_date)
            
            # Remove existing record/duplicate for same day
            st.session_state.student_attendance = st.session_state.student_attendance[
                ~((st.session_state.student_attendance["Student ID"] == sid) & 
                  (st.session_state.student_attendance["Date"] == date_str))
            ]
            
            # Add new record
            new_att = pd.DataFrame([{
                "Student ID": sid, 
                "Name": student_name, 
                "Class": selected_class, 
                "Date": date_str, 
                "Status": status
            }])
            
            st.session_state.student_attendance = pd.concat([st.session_state.student_attendance, new_att], ignore_index=True)
            save_data("student_attendance")
            st.success(f"Marked **{student_name}** as **{status}**")
            st.rerun() 

    # --- Table View Section ---
    st.divider()
    st.subheader("📊 Attendance History")
    
    # Filter View
    view_df = st.session_state.student_attendance
    
    # Filter by Class (always applied based on selection above)
    view_df = view_df[view_df["Class"] == selected_class]
    
    # Filter by Date (always applied based on selection above)
    # Ensure date column is string for comparison
    view_df = view_df[view_df["Date"] == str(att_date)]
    
    if not view_df.empty:
        try:
            st.dataframe(view_df.reset_index(drop=True), args={"width": "stretch"})
        except:
             st.dataframe(view_df.reset_index(drop=True), use_container_width=True)
    else:
        st.info(f"No attendance records for Class {selected_class} on {att_date}.")

def page_teacher_attendance():
    st.title("📋 Teacher Attendance")

    if st.session_state.teachers.empty:
        st.warning("⚠️ No teachers found. Please add teachers first.")
        return

    # --- Filter ---
    att_date = st.date_input("Select Date", date.today())

    # --- Mark Attendance Section ---
    st.divider()
    st.subheader("📝 Mark Attendance")

    teacher_name = st.selectbox("Select Teacher", st.session_state.teachers["Name"])
    
    # Status Buttons
    c1, c2, c3 = st.columns(3)
    status = None
    
    if c1.button("✅ Present", key="t_pres", use_container_width=True):
        status = "Present"
    if c2.button("❌ Absent", key="t_abs", use_container_width=True):
        status = "Absent"
    if c3.button("⚠️ Leave", key="t_leave", use_container_width=True):
        status = "Leave"
    
    if status:
        tid = st.session_state.teachers[st.session_state.teachers["Name"] == teacher_name].iloc[0]["Teacher ID"]
        date_str = str(att_date)
        
        # Remove existing record/duplicate for same day
        st.session_state.teacher_attendance = st.session_state.teacher_attendance[
            ~((st.session_state.teacher_attendance["Teacher ID"] == tid) & 
              (st.session_state.teacher_attendance["Date"] == date_str))
        ]
        
        # Add new record
        new_att = pd.DataFrame([{
            "Teacher ID": tid, 
            "Name": teacher_name, 
            "Date": date_str, 
            "Status": status
        }])
        
        st.session_state.teacher_attendance = pd.concat([st.session_state.teacher_attendance, new_att], ignore_index=True)
        save_data("teacher_attendance")
        st.success(f"Marked **{teacher_name}** as **{status}**")
        st.rerun()

    # --- Table View Section ---
    st.divider()
    st.subheader("📊 Attendance History")
    
    # Filter View
    view_df = st.session_state.teacher_attendance
    
    # Filter by Date
    view_df = view_df[view_df["Date"] == str(att_date)]
    
    if not view_df.empty:
        try:
            st.dataframe(view_df.reset_index(drop=True), args={"width": "stretch"})
        except:
             st.dataframe(view_df.reset_index(drop=True), use_container_width=True)
    else:
        st.info(f"No teacher attendance records for {att_date}.")

def page_student_results():
    st.title("📊 Student Results")
    
    if st.session_state.students.empty:
        st.warning("⚠️ No students found.")
        return

    # --- Select Student ---
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
    
    # --- Add Result Form ---
    st.divider()
    st.subheader("📝 Add New Result")
    
    with st.form("result_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            subject = st.selectbox("Subject", ["English", "Math", "Computer", "Urdu", "S.Study", "Science", "Islamiyat"])
        with c2:
            marks = st.number_input("Marks Obtained", min_value=0, max_value=100, step=1)
        
        submitted = st.form_submit_button("Save Result", use_container_width=True)
        
        if submitted:
            grade = (
                "A+" if marks >= 90 else
                "A" if marks >= 80 else
                "B" if marks >= 70 else
                "C" if marks >= 60 else
                "D" if marks >= 50 else
                "F"
            )
            
            sid = class_students[class_students["Name"] == student_name].iloc[0]["Student ID"]
            
            new_res = pd.DataFrame([{
                "Student ID": sid, 
                "Name": student_name, 
                "Subject": subject, 
                "Marks": marks, 
                "Grade": grade
            }])
            
            st.session_state.results = pd.concat([st.session_state.results, new_res], ignore_index=True)
            save_data("results")
            st.success(f"✅ Added: {subject} - {marks} ({grade})")
            st.rerun()

    # --- View Results Table ---
    st.divider()
    st.subheader(f"📜 Report Card: {student_name}")
    
    # Filter results for this student
    student_results = st.session_state.results[st.session_state.results["Name"] == student_name]
    
    if not student_results.empty:
        # Show specific columns
        display_df = student_results[["Subject", "Marks", "Grade"]]
        
        try:
            st.dataframe(display_df, args={"width": "stretch"}, hide_index=True)
        except:
             st.dataframe(display_df, use_container_width=True, hide_index=True)
             
        # Optional: Show Average
        avg_marks = student_results["Marks"].mean()
        st.caption(f"**Average Marks:** {avg_marks:.2f}")
    else:
        st.info("No results uploaded for this student yet.")

def page_view_records():
    st.title("📂 System Records")
    
    tab1, tab2, tab3, tab4 = st.tabs(["👨‍🎓 Students", "👩‍🏫 Teachers", "📅 Attendance", "📊 Results"])
    
    with tab1:
        if not st.session_state.students.empty:
            classes = sorted(st.session_state.students["Class"].unique().tolist(), key=lambda x: int(x) if x.isdigit() else x)
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
