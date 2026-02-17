# Masjid Attendance System

## Overview
A full-stack web app for managing student attendance in Ibadu Rahman Mosque. Teachers, admins, and stakeholders have role-specific dashboards and access.

## Features
- Multi-role login: Admin, Teacher, Stakeholder
- Mobile-friendly roll call
- Attendance dashboard with charts
- Admin panel for managing users and students

## Tech Stack
- Streamlit (Frontend)
- Python + psycopg2 (Backend)
- PostgreSQL (Database)
- Render (Deployment)
- Plotly (Charts)

## Setup
1. Clone repo
2. Create a virtual environment
3. Install requirements: `pip install -r requirements.txt`
4. Set environment variables:
   - `DB_HOST`
   - `DB_PORT`
   - `DB_USER`
   - `DB_PASSWORD`
   - `DB_NAME`
5. Run Streamlit: `streamlit run app.py`

## Live Demo
[Click here to view deployed app]((https://ibadu-rahman-attendance-1.onrender.com/))
