import streamlit as st
import pandas as pd
import plotly.express as px
from db import get_connection

def attendance_dashboard():
    st.title("📊 Attendance Dashboard")

    conn = get_connection()

    query = """
        SELECT 
            s.full_name,
            l.level_name,
            a.attendance_date,
            a.status
        FROM attendance a
        JOIN students s ON a.student_id = s.id
        JOIN levels l ON s.level_id = l.id
    """

    df = pd.read_sql(query, conn)
    conn.close()

    if df.empty:
        st.warning("No attendance records found.")
        return

    # Convert date
    df['attendance_date'] = pd.to_datetime(df['attendance_date'])

    # --- 1️⃣ Total Attendance by Status ---
    status_count = df['status'].value_counts().reset_index()
    status_count.columns = ['Status', 'Count']

    fig1 = px.pie(
        status_count,
        names='Status',
        values='Count',
        title="Overall Attendance Distribution"
    )

    st.plotly_chart(fig1, use_container_width=True)

    # --- 2️⃣ Attendance Over Time ---
    daily_attendance = df.groupby('attendance_date').size().reset_index(name='Count')

    fig2 = px.line(
        daily_attendance,
        x='attendance_date',
        y='Count',
        title="Daily Attendance Trend"
    )

    st.plotly_chart(fig2, use_container_width=True)

    # --- 3️⃣ Attendance by Level ---
    level_attendance = df.groupby('level_name').size().reset_index(name='Count')

    fig3 = px.bar(
        level_attendance,
        x='level_name',
        y='Count',
        title="Attendance by Level"
    )

    st.plotly_chart(fig3, use_container_width=True)
