import streamlit as st
from db import get_connection
from datetime import date

def teacher_panel():
    st.title("Teacher Roll Call")
    
    selected_date = st.date_input("Select Date", date.today())
    
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute("""
        SELECT s.id, s.full_name
        FROM students s
    """)
    students = cur.fetchall()
    
    attendance_data = {}
    
    for student_id, name in students:
        status = st.selectbox(
            f"{name}",
            ["Present", "Absent"],
            key=f"{student_id}"
        )
        attendance_data[student_id] = status
    
    if st.button("Submit Attendance"):
        for student_id, status in attendance_data.items():
            cur.execute("""
                INSERT INTO attendance (student_id, class_date, status, marked_by)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (student_id, class_date)
                DO UPDATE SET status = EXCLUDED.status
            """, (student_id, selected_date, status, st.session_state.user_id))
        
        conn.commit()
        cur.close()
        conn.close()
        
        st.success("Attendance submitted successfully")