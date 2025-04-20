# app.py
import streamlit as st
from utils import login_user, get_exams, register_user_to_exams, get_user_registrations

st.set_page_config(page_title="Exam Registration System", layout="centered")

st.title("📚 Exam Registration System")

if "user" not in st.session_state:
    st.session_state.user = None

# ---------------- LOGIN FORM ----------------
if st.session_state.user is None:
    st.subheader("🔐 Login")
    with st.form("login_form"):
        email = st.text_input("Email")
        phone = st.text_input("Phone")
        role = st.selectbox("Role", ["student", "admin"])
        submitted = st.form_submit_button("Login")

        if submitted:
            user = login_user(email, phone, role)
            if user:
                st.session_state.user = user
                st.success("Login successful")
                st.rerun()
            else:
                st.error("Invalid credentials")

# ---------------- STUDENT DASHBOARD ----------------
elif st.session_state.user["role"] == "student":
    st.subheader(f"🎓 Welcome, {st.session_state.user['name']}")

    exams = get_exams()
    exam_options = {exam["subject"]: exam["exam_id"] for exam in exams}
    selected_subjects = st.multiselect("Choose exams (max 5)", list(exam_options.keys()))

    if st.button("Register"):
        if len(selected_subjects) == 0:
            st.warning("Select at least one exam.")
        elif len(selected_subjects) > 5:
            st.warning("You can select up to 5 exams.")
        else:
            ids = [exam_options[sub] for sub in selected_subjects]
            success, msg = register_user_to_exams(st.session_state.user["user_id"], ids)
            if success:
                st.success(msg)
            else:
                st.error(msg)

    st.markdown("### 🗂️ Your Registrations")
    registrations = get_user_registrations(st.session_state.user["user_id"])
    st.table(registrations)

# ---------------- ADMIN DASHBOARD ----------------
elif st.session_state.user["role"] == "admin":
    st.subheader("🧾 All Student Registrations")

    from utils import get_all_registrations, cancel_registration
    registrations = get_all_registrations()

    for reg in registrations:
        st.write(f"👤 {reg['student_name']} | 📧 {reg['email']} | 📚 {reg['subject']} | 🗓️ {reg['registration_date']} | 📌 Status: {reg['status']}")
        if reg["status"] != "cancelled":
            if st.button(f"❌ Cancel Registration #{reg['registration_id']}", key=reg["registration_id"]):
                cancel_registration(reg["registration_id"])
                st.success(f"Cancelled Registration #{reg['registration_id']}")
                st.rerun()


if st.button("Logout"):
    st.session_state.user = None
    st.rerun()

