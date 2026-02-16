import streamlit as st
from auth import login_user
from admin import admin_panel
from teacher import teacher_panel
from stakeholder import stakeholder_panel

st.set_page_config(page_title="Masjid Attendance System")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login_page():
    st.title("Masjid Attendance Login")
    
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

if not st.session_state.logged_in:
    login_page()
else:
    st.sidebar.write(f"Welcome {st.session_state.name}")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()
    
    role = st.session_state.role
    
    if role == "admin":
        admin_panel()
    elif role == "teacher":
        teacher_panel()
    elif role == "stakeholder":
        stakeholder_panel()