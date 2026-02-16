import bcrypt
from db import get_connection

def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed.encode())

def login_user(email, password):
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute("SELECT id, full_name, password_hash, role FROM users WHERE email=%s", (email,))
    user = cur.fetchone()
    
    cur.close()
    conn.close()
    
    if user:
        user_id, name, stored_hash, role = user
        if verify_password(password, stored_hash):
            return user_id, name, role
    return None