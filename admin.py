import streamlit as st
from db import get_connection
from auth import hash_password

def admin_panel():
    st.title("Admin Panel")
    
    tab1, tab2 = st.tabs(["Register User", "Register Student"])
    
    # --------------------------
    # Tab 1: Register User
    # --------------------------
    with tab1:
        name = st.text_input("Full Name")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        role = st.selectbox("Role", ["admin", "teacher", "stakeholder"])
        
        if st.button("Create User"):
            conn = get_connection()
            cur = conn.cursor()
            
            hashed = hash_password(password)
            
            # ✅ Safe insert: ignore duplicate emails
            cur.execute("""
                INSERT INTO users (full_name, email, password_hash, role)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (email) DO NOTHING
            """, (name, email, hashed, role))
            
            conn.commit()
            cur.close()
            conn.close()
            
            st.success("User created successfully (or already exists)")
    
    # --------------------------
    # Tab 2: Register Student
    # --------------------------
    with tab2:
        student_name = st.text_input("Student Name")
        
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, level_name FROM levels")
        levels = cur.fetchall()
        cur.close()
        conn.close()
        
        level_dict = {level[1]: level[0] for level in levels}
        
        selected_level = st.selectbox("Level", list(level_dict.keys()))
        
        if st.button("Register Student"):
            conn = get_connection()
            cur = conn.cursor()
            
            # ✅ Safe insert: ignore duplicate student names for the same level
            cur.execute("""
                INSERT INTO students (full_name, level_id)
                VALUES (%s, %s)
                ON CONFLICT (full_name, level_id) DO NOTHING
            """, (student_name, level_dict[selected_level]))
            
            conn.commit()
            cur.close()
            conn.close()
            
            st.success("Student registered successfully (or already exists)")
