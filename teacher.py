import streamlit as st
from db import get_connection
from datetime import date

def teacher_panel():

    st.title("Teacher Roll Call")

    user_id = st.session_state.user_id

    # ---- Date & Session Selection ----
    col1, col2 = st.columns(2)

    with col1:
        selected_date = st.date_input("Select Date", date.today())

    with col2:
        selected_session = st.selectbox(
            "Select Session",
            ["Morning", "Afternoon", "Evening"]
        )

    # ---- Fetch Only Assigned Students ----
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT s.id, s.full_name
        FROM students s
        JOIN levels l ON s.level_id = l.id
        JOIN teacher_levels tl ON tl.level_id = l.id
        WHERE tl.teacher_id = %s
        ORDER BY s.full_name
    """, (user_id,))

    students = cur.fetchall()
    cur.close()
    conn.close()

    if not students:
        st.warning("No students assigned to you.")
        return

    st.subheader("Mark Attendance")

    # ---- Mark All Present Button ----
    if st.button("Mark All Present"):
        for student_id, _ in students:
            st.session_state[f"student_{student_id}"] = True
        st.rerun()

    attendance_data = {}

    present_count = 0

    # ---- Student Checkbox List ----
    for student_id, name in students:

        checked = st.checkbox(
            name,
            key=f"student_{student_id}"
        )

        attendance_data[student_id] = checked

        if checked:
            present_count += 1

    total_students = len(students)

    st.info(f"Present: {present_count} / {total_students}")

    # ---- Save Attendance ----
    if st.button("Save Attendance"):

        conn = get_connection()
        cur = conn.cursor()

        for student_id, present in attendance_data.items():

            status = "Present" if present else "Absent"

            cur.execute("""
                INSERT INTO attendance 
                (student_id, class_date, session, status, marked_by)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (student_id, class_date, session)
                DO UPDATE SET 
                    status = EXCLUDED.status,
                    marked_by = EXCLUDED.marked_by,
                    updated_at = CURRENT_TIMESTAMP
            """, (
                student_id,
                selected_date,
                selected_session,
                status,
                user_id
            ))

        conn.commit()
        cur.close()
        conn.close()

        st.success("Attendance saved successfully!")
