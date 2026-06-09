import cv2

def draw_ui(frame, user_gesture, machine_move, user_score, machine_score, username, countdown=None, result_text=None):
    h, w = frame.shape[:2]

    # Background bar at top
    cv2.rectangle(frame, (0, 0), (w, 80), (0, 0, 0), -1)

    # Scores
    cv2.putText(frame, f"{username}: {user_score}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
    cv2.putText(frame, f"Machine: {machine_score}", (10, 65),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

    # Detected gesture
    cv2.putText(frame, f"Your move: {user_gesture}", (w - 280, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)

    # Machine move
    cv2.putText(frame, f"Machine move: {machine_move}", (w - 280, 65),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 100, 0), 2)

    # Countdown
    if countdown is not None:
        cv2.putText(frame, str(countdown), (w // 2 - 30, h // 2),
                    cv2.FONT_HERSHEY_SIMPLEX, 4, (0, 255, 255), 6)

    # Round result
    if result_text is not None:
        cv2.putText(frame, result_text, (w // 2 - 150, h - 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 3)

    return frame