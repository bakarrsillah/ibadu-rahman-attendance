import streamlit as st
from db import get_connection

def stakeholder_panel():
    st.title("Attendance Overview")
    
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute("SELECT id, full_name FROM students")
    students = cur.fetchall()
    
    student_dict = {s[1]: s[0] for s in students}
    
    selected_student = st.selectbox("Select Student", list(student_dict.keys()))
    
    student_id = student_dict[selected_student]
    
    cur.execute("""
        SELECT 
            COUNT(*) FILTER (WHERE status='Present') * 100.0 /
            NULLIF(COUNT(*),0)
        FROM attendance
        WHERE student_id = %s
    """, (student_id,))
    
    percentage = cur.fetchone()[0]
    
    cur.close()
    conn.close()
    
    if percentage:
        st.metric("Attendance Percentage", f"{percentage:.2f}%")
    else:
        st.metric("Attendance Percentage", "0%")