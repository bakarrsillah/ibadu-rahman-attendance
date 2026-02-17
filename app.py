import streamlit as st
from auth import login_user
from admin import admin_panel
from teacher import teacher_panel
from stakeholder import stakeholder_panel
from dashboard import attendance_dashboard

st.set_page_config(page_title="Ibadu Rahman Masjid Attendance System")

# ---------------- SESSION INIT ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ---------------- LOGIN PAGE ----------------
def login_page():
    st.title("Masjid Attendance System")
    st.subheader("Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        result = login_user(email, password)

        if result:
            user_id, name, role = result
            st.session_state.logged_in = True
            st.session_state.user_id = user_id
            st.session_state.name = name
            st.session_state.role = role
            st.success("Login successful")
            st.rerun()
        else:
            st.error("Invalid credentials")

# ---------------- MAIN ROUTING ----------------
if not st.session_state.logged_in:
    login_page()

else:
    st.sidebar.title("Masjid Attendance")
    st.sidebar.write(f"Welcome {st.session_state.name}")

    if st.sidebar.button("Logout"):
        st.session_state.clear()
        st.rerun()

    role = st.session_state.role

    # ================= ADMIN =================
    if role == "admin":

        page = st.sidebar.selectbox(
            "Navigation",
            ["Admin Panel", "Dashboard"]
        )

        if page == "Admin Panel":
            admin_panel()

        elif page == "Dashboard":
            attendance_dashboard()

    # ================= TEACHER =================
    elif role == "teacher":

        page = st.sidebar.selectbox(
            "Navigation",
            ["Roll Call", "Dashboard"]
        )

        if page == "Roll Call":
            teacher_panel()

        elif page == "Dashboard":
            attendance_dashboard()

    # ================= STAKEHOLDER =================
    elif role == "stakeholder":

        page = st.sidebar.selectbox(
            "Navigation",
            ["Dashboard"]
        )

        if page == "Dashboard":
            attendance_dashboard()
