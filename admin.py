import streamlit as st
from db import get_connection
from auth import hash_password

def admin_panel():

    st.title("Admin Panel")

    tab1, tab2, tab3 = st.tabs([
        "Register User",
        "Register Student",
        "Assign Teacher to Level"
    ])

    # ---------------- REGISTER USER ----------------
    with tab1:

        name = st.text_input("Full Name")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        role = st.selectbox("Role", ["admin", "teacher", "stakeholder"])

        if st.button("Create User"):

            conn = get_connection()
            cur = conn.cursor()

            hashed = hash_password(password)

            try:
                cur.execute("""
                    INSERT INTO users (full_name, email, password_hash, role)
                    VALUES (%s, %s, %s, %s)
                """, (name, email, hashed, role))

                conn.commit()
                st.success("User created successfully")

            except Exception as e:
                st.error(f"Error: {e}")

            cur.close()
            conn.close()

    # ---------------- REGISTER STUDENT ----------------
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

            try:
                cur.execute("""
                    INSERT INTO students (full_name, level_id)
                    VALUES (%s, %s)
                """, (student_name, level_dict[selected_level]))

                conn.commit()
                st.success("Student registered successfully")

            except Exception as e:
                st.error(f"Error: {e}")

            cur.close()
            conn.close()

    # ---------------- ASSIGN TEACHER TO LEVEL ----------------
    with tab3:

        conn = get_connection()
        cur = conn.cursor()

        # Get Teachers
        cur.execute("""
            SELECT id, full_name 
            FROM users 
            WHERE role = 'teacher'
        """)
        teachers = cur.fetchall()

        # Get Levels
        cur.execute("SELECT id, level_name FROM levels")
        levels = cur.fetchall()

        cur.close()
        conn.close()

        if not teachers:
            st.warning("No teachers found.")
            return

        teacher_dict = {t[1]: t[0] for t in teachers}
        level_dict = {l[1]: l[0] for l in levels}

        selected_teacher = st.selectbox("Select Teacher", list(teacher_dict.keys()))
        selected_level = st.selectbox("Select Level", list(level_dict.keys()))

        if st.button("Assign Teacher"):

            conn = get_connection()
            cur = conn.cursor()

            try:
                cur.execute("""
                    INSERT INTO teacher_levels (teacher_id, level_id)
                    VALUES (%s, %s)
                    ON CONFLICT (teacher_id, level_id) DO NOTHING
                """, (
                    teacher_dict[selected_teacher],
                    level_dict[selected_level]
                ))

                conn.commit()
                st.success("Teacher assigned successfully")

            except Exception as e:
                st.error(f"Error: {e}")

            cur.close()
            conn.close()
