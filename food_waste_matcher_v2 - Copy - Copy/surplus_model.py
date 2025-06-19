import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import pickle

# Sample training data
data = {
    "Expected_People": [200, 300, 150, 400, 250, 180],
    "Actual_People": [150, 280, 100, 250, 230, 140],
    "Duration": [4, 5, 3, 6, 3, 2],
    "Event_Type": ["Wedding", "Corporate", "Birthday", "Festival", "Corporate", "Wedding"],
    "Food_Type": ["Veg", "Mixed", "Veg", "Mixed", "Veg", "Mixed"],
    "Surplus_Kgs": [50, 20, 30, 100, 15, 35]
}

df = pd.DataFrame(data)

# One-hot encoding
df = pd.get_dummies(df, columns=["Event_Type", "Food_Type"])

# Train the model
X = df.drop("Surplus_Kgs", axis=1)
y = df["Surplus_Kgs"]

model = RandomForestRegressor()
model.fit(X, y)

# Save model
with open("surplus_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("✅ Model trained and saved as surplus_model.pkl")
