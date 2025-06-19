import streamlit as st
import pandas as pd
import pickle
from firebase_utils import store_supplier_data

def supplier_page():
    st.markdown("<h2 style='color:#228B22;'>🍱 Supplier Form</h2>", unsafe_allow_html=True)

    event_type = st.selectbox("📅 Event Type", ["Wedding", "Corporate", "Birthday", "Festival"])
    food_type = st.selectbox("🍛 Food Type", ["Veg", "Mixed"])
    expected = st.number_input("Expected People", 10, 1000)
    actual = st.number_input("Actual People", 0, expected)
    duration = st.number_input("Event Duration (hours)", 1, 12)
    latitude = st.number_input("📍 Event Latitude", format="%.6f")
    longitude = st.number_input("📍 Event Longitude", format="%.6f")

    if st.button("Predict Surplus & Submit"):
        model = pickle.load(open("surplus_model.pkl", "rb"))
        df_input = pd.DataFrame([[expected, actual, duration, event_type, food_type]],
                                columns=["Expected_People", "Actual_People", "Duration", "Event_Type", "Food_Type"])
        df_input = pd.get_dummies(df_input)

        for col in model.feature_names_in_:
            if col not in df_input:
                df_input[col] = 0
        df_input = df_input[model.feature_names_in_]

        surplus = model.predict(df_input)[0]
        st.success(f"Estimated Surplus: {surplus:.2f} Kg")

        data = {
            "email": st.session_state.email,
            "expected": expected,
            "actual": actual,
            "duration": duration,
            "event_type": event_type,
            "food_type": food_type,
            "latitude": latitude,
            "longitude": longitude,
            "surplus": float(surplus)
        }
        store_supplier_data(data)
        st.success("✅ Data stored in Firebase.")
