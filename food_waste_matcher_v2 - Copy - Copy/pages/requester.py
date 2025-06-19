import streamlit as st
from firebase_utils import get_suppliers_nearby

def requester_page():
    st.markdown("<h2 style='color:#1E90FF;'>📥 Requester Form</h2>", unsafe_allow_html=True)
    needed_kg = st.number_input("🍚 Amount of Food Needed (Kg)", min_value=1.0)
    latitude = st.number_input("📍 Your Location Latitude", format="%.6f")
    longitude = st.number_input("📍 Your Location Longitude", format="%.6f")

    if st.button("Find Nearby Surplus"):
        matches = get_suppliers_nearby(needed_kg, (latitude, longitude))
        if matches:
            st.success("✅ Matching Suppliers:")
            for m in matches:
                st.write(f"📍 {m['email']} | Surplus: {m['surplus']} Kg | Distance: {m['distance']} km")
        else:
            st.warning("❌ No matching suppliers found.")
