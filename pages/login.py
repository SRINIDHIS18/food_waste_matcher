import streamlit as st
from firebase_utils import firebase_login, get_user_role

def login_page():
    st.markdown("<h2 style='color:#4B0082;'>🔐 Login to Food Matcher</h2>", unsafe_allow_html=True)
    with st.form("login_form"):
        email = st.text_input("📧 Email", placeholder="you@example.com")
        password = st.text_input("🔑 Password", type="password", placeholder="Enter password")
        submitted = st.form_submit_button("Login", type="primary")
        
        if submitted:
            user = firebase_login(email, password)
            if user:
                st.session_state.auth = True
                st.session_state.email = email
                role = get_user_role(email)
                st.session_state.role = role
                st.success(f"✅ Logged in as {role}")
            else:
                st.error("❌ Login failed. Check credentials.")
