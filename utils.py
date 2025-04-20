from db import get_connection
from datetime import datetime

def login_user(email, phone, role):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE email=%s AND phone=%s AND role=%s", (email, phone, role))
    user = cursor.fetchone()
    conn.close()
    return user

def get_exams():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM exams")
    exams = cursor.fetchall()
    conn.close()
    return exams

def register_user_to_exams(user_id, selected_exam_ids):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT wallet FROM users WHERE user_id=%s", (user_id,))
    result = cursor.fetchone()
    if not result:
        return False, "User not found"
    
    wallet = result["wallet"]
    total = 100 * len(selected_exam_ids)

    if wallet < total:
        return False, "Insufficient balance"

    for exam_id in selected_exam_ids:
        cursor.execute(
            "INSERT INTO registrations (user_id, exam_id, registration_date) VALUES (%s, %s, %s)",
            (user_id, exam_id, datetime.today().strftime('%Y-%m-%d'))
        )
    
    cursor.execute("UPDATE users SET wallet = wallet - %s WHERE user_id = %s", (total, user_id))
    conn.commit()
    conn.close()
    return True, "Registration successful"

def get_user_registrations(user_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT r.registration_id, r.status, r.registration_date, r.cancel_reason, e.subject
        FROM registrations r
        JOIN exams e ON r.exam_id = e.exam_id
        WHERE r.user_id = %s
    """, (user_id,))
    data = cursor.fetchall()
    conn.close()
    return data

# ---------------- ADMIN FUNCTIONS ----------------

def get_all_registrations():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT 
            r.registration_id,
            u.name AS student_name,
            u.email,
            e.subject,
            r.registration_date,
            r.status
        FROM registrations r
        JOIN users u ON r.user_id = u.user_id
        JOIN exams e ON r.exam_id = e.exam_id
        ORDER BY r.registration_date DESC;
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows

def cancel_registration(registration_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE registrations SET status = 'cancelled' WHERE registration_id = %s", (registration_id,))
    conn.commit()
    conn.close()

