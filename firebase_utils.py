import pyrebase
import firebase_admin
from firebase_admin import credentials, db
from geopy.distance import geodesic
import time


firebase_config = {
    "apiKey": "YOUR_API_KEY",
    "authDomain": "YOUR_AUTH_DOMAIN",
    "databaseURL": "YOUR_DATABASE_URL",
    "projectId": "YOUR_PROJECT_ID",
    "storageBucket": "YOUR_STORAGE_BUCKET",
    
}


firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()
db_url = firebase_config["databaseURL"]


cred = credentials.Certificate("serviceAccountKey.json")
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred, {'databaseURL': db_url})



def firebase_login(email, password):
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        return user
    except Exception as e:
        print("Login error:", e)
        return None



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



def get_user_role(email):
    ref = db.reference("roles")
    roles = ref.get()
    if roles:
        for uid, info in roles.items():
            if info.get("email") == email:
                return info.get("role")
    return None



def delete_old_supplier_events():
    ref = db.reference("supplier_events")
    events = ref.get()
    if events:
        now = time.time()
        for key, val in events.items():
            timestamp = val.get("timestamp")
            if timestamp and (now - timestamp) > 21600:  
                ref.child(key).delete()



def store_supplier_data(data):
    data["timestamp"] = time.time()
    ref = db.reference("supplier_events")
    ref.push(data)
    delete_old_supplier_events()



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
