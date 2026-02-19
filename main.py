import streamlit as st
import pandas as pd
import utils 

# -----------------------------------------------------------------------------
# 1. APP CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Sun Shine School System",
    page_icon="🏫",
    layout="centered"
)

# -----------------------------------------------------------------------------
# 2. LOAD RESOURCES
# -----------------------------------------------------------------------------
# Load CSV data into Session State
utils.load_data()

# Apply Custom CSS for Buttons, Sidebar, and Backgrounds
utils.apply_styling()

# -----------------------------------------------------------------------------
# 3. SIDEBAR & NAVIGATION
# -----------------------------------------------------------------------------
current_page = utils.sidebar_navigation()

# -----------------------------------------------------------------------------
# 4. MAIN PAGE ROUTING
# -----------------------------------------------------------------------------

def handle_routing():
    """ Determines which page to show based on user selection """
    
    if current_page == "Dashboard":
        utils.page_dashboard()

    elif current_page == "Add Student":
        st.markdown("### 🎓 Student Enrollment")
        # Logic to add student is handled in utils to keep main clean
        utils.page_add_student()

    elif current_page == "Add Teacher":
        st.markdown("### 🍎 Teacher Registration")
        utils.page_add_teacher()

    elif current_page == "Student Attendance":
        st.markdown("### 📅 Daily Student Attendance")
        
        # We can perform some pre-checks here in main.py to show Teacher logic
        if st.session_state.students.empty:
            st.warning("⚠️ No students found. Please add students first.")
        else:
            utils.page_student_attendance()

    elif current_page == "Teacher Attendance":
        st.markdown("### 📋 Teacher Attendance Log")
        utils.page_teacher_attendance()

    elif current_page == "Student Results":
        st.markdown("### 📊 Examination Results")
        utils.page_student_results()

    elif current_page == "View Records":
        st.markdown("### 📂 System Database")
        utils.page_view_records()

# Run the app logic
handle_routing()

# -----------------------------------------------------------------------------
# 5. FOOTER (Optional)
# -----------------------------------------------------------------------------
st.markdown("---")
st.caption("© 2026 Sun Shine School Management System | Developed by Anas")