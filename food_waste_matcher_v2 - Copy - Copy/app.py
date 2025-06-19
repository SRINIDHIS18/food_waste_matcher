import streamlit as st
from pages.login import login_page
from pages.register import register_page
from pages.supplier import supplier_page
from pages.requester import requester_page
from pages.logout import logout_page
from geopy.geocoders import Nominatim

# ⚠️ Streamlit page setup
st.set_page_config(page_title="Food Waste Matcher V2", page_icon="🍽️", layout="centered")

# 🎨 Custom CSS
st.markdown("""
    <style>
        body {
            background-color: #f7f7f7;
        }
        .stButton button {
            background-color: #6A5ACD;
            color: white;
            border-radius: 10px;
        }
        .stButton button:hover {
            background-color: #7B68EE;
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

# 🔒 Session state
if "auth" not in st.session_state:
    st.session_state.auth = False
    st.session_state.role = None
    st.session_state.email = ""

# 📍 Location chatbot logic
def get_coordinates(place_name):
    geolocator = Nominatim(user_agent="food_waste_matcher_app")
    try:
        location = geolocator.geocode(place_name)
        if location:
            return location.latitude, location.longitude
        else:
            return None, None
    except Exception as e:
        return None, None

# 🧭 Sidebar navigation
st.sidebar.title("🍽️ Food Matcher")

# Chatbot inside sidebar
with st.sidebar.expander("💬 Location Chatbot (Ask Place Name)", expanded=False):
    chatbot_query = st.text_input("Enter a place name:")
    if chatbot_query:
        lat, lon = get_coordinates(chatbot_query)
        if lat and lon:
            st.sidebar.success(f"📍 {chatbot_query}\nLat: {lat:.4f}, Lon: {lon:.4f}")
        else:
            st.sidebar.warning("⚠️ Place not found. Try a more specific name.")

# Sidebar menu options based on login state
if st.session_state.auth:
    page = st.sidebar.selectbox("Navigate", ["Supplier", "Requester", "Logout"])
else:
    page = st.sidebar.selectbox("Navigate", ["Login", "Register"])

# 🚦 Page Routing
if page == "Login":
    login_page()
elif page == "Register":
    register_page()
elif page == "Supplier" and st.session_state.role == "supplier":
    supplier_page()
elif page == "Requester" and st.session_state.role == "requester":
    requester_page()
elif page == "Logout":
    logout_page()
else:
    st.warning("⚠️ Please login to access this page.")
