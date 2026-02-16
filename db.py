import psycopg2

def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="masjid_attendance",
        user="masjid_attendance_user",
        password="a2F9Lmkxv6usvAQ8yCoqplHJTxnxM4Cw",
        port="5432"
    )