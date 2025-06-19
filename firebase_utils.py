import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
from geopy.distance import geodesic
import time
import pyrebase
import json

# 🔐 Load Firebase Admin SDK credentials from secrets
cred_dict = dict(st.secrets["firebase"])
cred = credentials.Certificate(cred_dict)

# ✅ Initialize Firebase Admin (for Realtime DB)
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred, {
        'databaseURL': cred_dict["databaseURL"]
    })

# ✅ Initialize Pyrebase (for Authentication)
firebase_config = {
    "apiKey": cred_dict.get("apiKey", ""),  # optional, if included in secrets
    "authDomain": cred_dict.get("authDomain", ""),
    "databaseURL": cred_dict["databaseURL"],
    "projectId": cred_dict.get("project_id", ""),
    "storageBucket": cred_dict.get("storageBucket", ""),
}
firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()

# 🔑 Login user
def firebase_login(email, password):
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        return user
    except Exception as e:
        print("Login error:", e)
        return None

# 📝 Register user and store role with UID
def firebase_register(email, password, role):
    try:
        user = auth.create_user_with_email_and_password(email, password)
        uid = user['localId']
        role_ref = db.reference(f"roles/{uid}")
        role_ref.set({
            "email": email,
            "role": role
        })
        return user
    except Exception as e:
        print("Registration error:", e)
        return None

# 🔍 Get user role from Realtime DB
def get_user_role(email):
    ref = db.reference("roles")
    roles = ref.get()
    if roles:
        for uid, info in roles.items():
            if info.get("email") == email:
                return info.get("role")
    return None

# 🕒 Auto-delete supplier events older than 6 hours
def delete_old_supplier_events():
    ref = db.reference("supplier_events")
    events = ref.get()
    if events:
        now = time.time()
        for key, val in events.items():
            timestamp = val.get("timestamp")
            if timestamp and (now - timestamp) > 21600:
                ref.child(key).delete()

# 📥 Store supplier event data with timestamp
def store_supplier_data(data):
    data["timestamp"] = time.time()
    ref = db.reference("supplier_events")
    ref.push(data)
    delete_old_supplier_events()

# 📍 Find nearby supplier matches
def get_suppliers_nearby(required_kg, location, radius_km=10):
    ref = db.reference("supplier_events")
    events = ref.get()
    matches = []
    if events:
        for key, val in events.items():
            try:
                supplier_loc = (val['latitude'], val['longitude'])
                dist = geodesic(location, supplier_loc).km
                if dist <= radius_km and abs(val['surplus'] - required_kg) <= 5:
                    val['distance'] = round(dist, 2)
                    matches.append(val)
            except Exception as e:
                print("Error in matching:", e)
    return matches
