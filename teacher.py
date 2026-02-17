import streamlit as st
from db import get_connection
from datetime import date

def teacher_panel():
    st.title("📋 Teacher Roll Call")
    
    selected_date = st.date_input("Select Date", date.today())
    
    conn = get_connection()
    cur = conn.cursor()
    
    # Get teacher's assigned levels
    cur.execute("""
        SELECT level_id
        FROM teacher_levels
        WHERE teacher_id = %s
    """, (st.session_state.user_id,))
    levels = [row[0] for row in cur.fetchall()]
    
    # Get students in those levels
    if levels:
        cur.execute(f"""
            SELECT id, full_name
            FROM students
            WHERE level_id = ANY(%s)
            ORDER BY full_name
        """, (levels,))
        students = cur.fetchall()
    else:
        students = []
    
    cur.close()
    conn.close()
    
    st.write(f"Total students: {len(students)}")
    
    # Initialize attendance in session_state
    if "attendance" not in st.session_state:
        st.session_state.attendance = {student[0]: False for student in students}  # False = Absent
    
    # Layout buttons in columns (3 per row)
    cols_per_row = 3
    for i in range(0, len(students), cols_per_row):
        cols = st.columns(cols_per_row)
        for j, student in enumerate(students[i:i+cols_per_row]):
            student_id, name = student
            present = st.session_state.attendance[student_id]
            
            # Button label and color
            label = name
            button_color = "✅ " if present else "⬜ "
            
            # Button to toggle
            if cols[j].button(f"{button_color}{label}", key=f"att_{student_id}"):
                st.session_state.attendance[student_id] = not st.session_state.attendance[student_id]
    
    # "Mark All Present" button
    if st.button("Mark All Present"):
        for student_id in st.session_state.attendance.keys():
            st.session_state.attendance[student_id] = True
    
    # Submit attendance
    if st.button("Submit Attendance"):
        conn = get_connection()
        cur = conn.cursor()
        
        for student_id, present in st.session_state.attendance.items():
            status = "Present" if present else "Absent"
            cur.execute("""
                INSERT INTO attendance (student_id, class_date, session, status, marked_by)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (student_id, class_date, session)
                DO UPDATE SET status = EXCLUDED.status, updated_at = CURRENT_TIMESTAMP, updated_by = EXCLUDED.marked_by
            """, (student_id, selected_date, 'Morning', status, st.session_state.user_id))
        
        conn.commit()
        cur.close()
        conn.close()
        st.success("Attendance submitted successfully!")
