import pandas as pd
import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import accuracy_score, classification_report
import pickle
import os

# Load data
print("📂 Loading data...")
df = pd.read_csv("gesture_data.csv")

X = df.drop("label", axis=1).values
y = df["label"].values

# Encode labels
le = LabelEncoder()
y_encoded = le.fit_transform(y)

# Scale features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y_encoded, test_size=0.2, random_state=42
)

# Build MLP model
print("🧠 Training MLP Neural Network...")
model = MLPClassifier(
    hidden_layer_sizes=(256, 128, 64, 32),
    activation='relu',
    max_iter=1000,
    random_state=42,
    learning_rate='adaptive',
    verbose=True
)

model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"\n✅ Accuracy: {accuracy * 100:.2f}%")
print("\n📊 Classification Report:")
print(classification_report(y_test, y_pred, target_names=le.classes_))

# Save model, scaler and label encoder
print("\n💾 Saving model...")
with open("gesture_model.pkl", "wb") as f:
    pickle.dump(model, f)

with open("gesture_scaler.pkl", "wb") as f:
    pickle.dump(scaler, f)

with open("gesture_encoder.pkl", "wb") as f:
    pickle.dump(le, f)

print("✅ Model saved as gesture_model.pkl")
print("✅ Scaler saved as gesture_scaler.pkl")
print("✅ Encoder saved as gesture_encoder.pkl")