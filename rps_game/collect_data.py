import cv2
import mediapipe as mp
import csv
import os
import time

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

CSV_FILE = "gesture_data.csv"

def get_landmarks(frame):
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)
    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            landmarks = []
            for lm in hand_landmarks.landmark:
                landmarks.extend([lm.x, lm.y, lm.z])
            return frame, landmarks
    return frame, None

def collect(label, samples=100):
    cap = cv2.VideoCapture(0)
    count = 0

    print(f"\n📸 Collecting {samples} samples for: {label.upper()}")
    print("Get ready... starting in 3 seconds")
    time.sleep(3)

    with open(CSV_FILE, "a", newline="") as f:
        writer = csv.writer(f)

        while count < samples:
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.flip(frame, 1)
            frame, landmarks = get_landmarks(frame)

            cv2.putText(frame, f"Collecting: {label.upper()} ({count}/{samples})",
                        (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.imshow("Data Collection", frame)

            if landmarks:
                writer.writerow([label] + landmarks)
                count += 1

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()
    print(f"✅ Done collecting {label.upper()}")

if __name__ == "__main__":
    # Create CSV with header if not exists
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            header = ["label"] + [f"{axis}{i}" for i in range(21) for axis in ["x", "y", "z"]]
            writer.writerow(header)

    print("=== Gesture Data Collection ===")
    print("You will collect 100 samples for each gesture")
    print("Show the gesture clearly in front of the camera\n")

    for gesture in ["rock", "paper", "scissors"]:
        input(f"Press ENTER when ready to collect: {gesture.upper()}")
        collect(gesture, samples=100)

    print("\n✅ All gestures collected! gesture_data.csv is ready.")