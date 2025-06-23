import streamlit as st

def logout_page():
    st.session_state.auth = False
    st.session_state.email = ""
    st.session_state.role = None
    st.success("🔓 You have been logged out.")
