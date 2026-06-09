import cv2
import mediapipe as mp
import numpy as np
import pickle

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

# Load MLP model, scaler and encoder
with open("gesture_model.pkl", "rb") as f:
    model = pickle.load(f)

with open("gesture_scaler.pkl", "rb") as f:
    scaler = pickle.load(f)

with open("gesture_encoder.pkl", "rb") as f:
    le = pickle.load(f)

def detect_gesture(frame):
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)
    gesture = "none"

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Extract landmarks
            landmarks = []
            for lm in hand_landmarks.landmark:
                landmarks.extend([lm.x, lm.y, lm.z])

            # Scale and predict
            landmarks_scaled = scaler.transform([landmarks])
            prediction = model.predict(landmarks_scaled)
            gesture = le.inverse_transform(prediction)[0]

    return frame, gesture