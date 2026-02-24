import streamlit as st
import pandas as pd
import os

USERS_FILE = "users.csv"

# ── Role permission map ────────────────────────────────────────────────────────
# Each role lists the page keys it is allowed to see
ROLE_PAGES = {
    "admin": [
        "Dashboard",
        "Add Student",
        "Add Teacher",
        "Student Attendance",
        "Teacher Attendance",
        "Student Results",
        "View Records",
        "Manage Users",
    ],
    "principal": [
        "Dashboard",
        "Add Student",
        "Add Teacher",
        "Student Attendance",
        "Teacher Attendance",
        "Student Results",
        "View Records",
    ],
    "teacher": [
        "Dashboard",
        "Student Attendance",
        "Student Results",
    ],
}


def load_users() -> pd.DataFrame:
    """Load users from CSV. Creates default file if missing."""
    if os.path.exists(USERS_FILE):
        return pd.read_csv(USERS_FILE, dtype=str).fillna("")
    # Create a minimal default file
    df = pd.DataFrame([
        {"username": "admin",     "password": "admin123",     "role": "admin",     "name": "System Admin"},
        {"username": "principal", "password": "principal123", "role": "principal", "name": "Mr. Principal"},
        {"username": "teacher",   "password": "teacher123",   "role": "teacher",   "name": "Ms. Teacher"},
    ])
    df.to_csv(USERS_FILE, index=False)
    return df


def save_users(df: pd.DataFrame):
    df.to_csv(USERS_FILE, index=False)


def authenticate(username: str, password: str):
    """
    Returns the user row dict on success, or None on failure.
    Case-insensitive username match.
    """
    users = load_users()
    match = users[users["username"].str.lower() == username.strip().lower()]
    if match.empty:
        return None
    user = match.iloc[0]
    if user["password"] == password:
        return user.to_dict()
    return None


def is_logged_in() -> bool:
    return st.session_state.get("logged_in", False)


def get_current_user() -> dict:
    return st.session_state.get("auth_user", {})


def get_role() -> str:
    return get_current_user().get("role", "")


def can_access(page: str) -> bool:
    role = get_role()
    return page in ROLE_PAGES.get(role, [])


def get_allowed_pages() -> list:
    role = get_role()
    return ROLE_PAGES.get(role, [])


def login(user_dict: dict):
    st.session_state.logged_in = True
    st.session_state.auth_user = user_dict
    st.session_state.current_page = "Dashboard"


def logout():
    for key in ["logged_in", "auth_user", "current_page"]:
        st.session_state.pop(key, None)
    st.rerun()
