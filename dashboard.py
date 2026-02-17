import streamlit as st
import pandas as pd
import plotly.express as px
from db import get_connection

def attendance_dashboard():
    st.title("📊 Attendance Dashboard")

    conn = get_connection()

    # Corrected query with class_date and session
    query = """
        SELECT 
            s.full_name,
            l.level_name,
            a.class_date,
            a.session,
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

    # Convert class_date to datetime
    df['class_date'] = pd.to_datetime(df['class_date'])

    # --- 1️⃣ Overall Attendance Distribution ---
    status_count = df['status'].value_counts().reset_index()
    status_count.columns = ['Status', 'Count']

    fig1 = px.pie(
        status_count,
        names='Status',
        values='Count',
        title="Overall Attendance Distribution"
    )
    st.plotly_chart(fig1, use_container_width=True)

    # --- 2️⃣ Daily Attendance Trend ---
    daily_attendance = df.groupby('class_date').size().reset_index(name='Count')

    fig2 = px.line(
        daily_attendance,
        x='class_date',
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

    # --- 4️⃣ Attendance by Session (Morning/Afternoon/Evening) ---
    session_attendance = df.groupby('session').size().reset_index(name='Count')

    fig4 = px.bar(
        session_attendance,
        x='session',
        y='Count',
        title="Attendance by Session"
    )
    st.plotly_chart(fig4, use_container_width=True)
