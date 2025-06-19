import streamlit as st
from firebase_utils import firebase_register
import smtplib
import random
from email.mime.text import MIMEText

def register_page():
    st.markdown("<h2 style='color:#DC143C;'>📝 Register</h2>", unsafe_allow_html=True)

    if "otp_sent" not in st.session_state:
        st.session_state.otp_sent = False
    if "generated_otp" not in st.session_state:
        st.session_state.generated_otp = None

    def send_otp_email(recipient_email, otp):
        sender_email = st.secrets["gmail"]["email"]
        sender_password = st.secrets["gmail"]["password"]

        message = MIMEText(f"Your OTP for Food Waste Matcher is: {otp}")
        message["Subject"] = "🔐 Your OTP Code"
        message["From"] = sender_email
        message["To"] = recipient_email

        try:
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.send_message(message)
            return True
        except Exception as e:
            st.error(f"Failed to send OTP: {e}")
            return False

    with st.form("register_form"):
        email = st.text_input("📧 Email", placeholder="newuser@example.com")
        password = st.text_input("🔒 Password", type="password", placeholder="Choose password")
        role = st.selectbox("🧑 Role", ["supplier", "requester"])

        if not st.session_state.otp_sent:
            send_otp = st.form_submit_button("📨 Send OTP", type="primary")
            if send_otp:
                if email:
                    otp = str(random.randint(100000, 999999))
                    if send_otp_email(email, otp):
                        st.session_state.generated_otp = otp
                        st.session_state.otp_sent = True
                        st.success("✅ OTP sent to your email.")
                else:
                    st.warning("⚠️ Please enter a valid email before requesting OTP.")
        else:
            entered_otp = st.text_input("🔑 Enter OTP", max_chars=6)
            verify_and_register = st.form_submit_button("✅ Verify & Register", type="primary")
            if verify_and_register:
                if entered_otp == st.session_state.generated_otp:
                    user = firebase_register(email, password, role)
                    if user:
                        st.success("🎉 Registration successful! You can now log in.")
                        st.session_state.otp_sent = False
                    else:
                        st.error("❌ Firebase registration failed.")
                else:
                    st.error("🚫 Incorrect OTP. Please try again.")
