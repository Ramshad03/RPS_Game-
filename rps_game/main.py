import cv2
import time
import threading
from gesture import detect_gesture
from game_logic import GameState, get_machine_move, get_round_result
from voice import say_game_start, say_user_scores, say_machine_scores, say_user_wins, say_machine_wins, say_draw, say_welcome, say_countdown
from gui import GameGUI

def run_game(username, gui):
    game = GameState(username)
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    say_welcome(username)
    time.sleep(2)
    say_game_start(username)
    time.sleep(2)

    round_active = True
    countdown_start = None
    countdown_value = None
    machine_move = "-"
    user_gesture = "-"
    result_text = None
    result_display_start = None
    countdown_spoken = []

    COUNTDOWN_SECONDS = 3
    RESULT_DISPLAY_TIME = 2

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        frame, detected_gesture = detect_gesture(frame)

        now = time.time()

        # Start new round
        if round_active and countdown_start is None:
            countdown_start = now
            countdown_value = COUNTDOWN_SECONDS
            result_text = None
            machine_move = "-"
            user_gesture = "-"
            countdown_spoken = []

        # Speak each countdown number in sync
        if countdown_start is not None:
            elapsed = now - countdown_start
            remaining = COUNTDOWN_SECONDS - int(elapsed)
            if remaining > 0 and remaining not in countdown_spoken:
                say_countdown(remaining)
                countdown_spoken.append(remaining)

        # Countdown phase
        if countdown_start is not None:
            elapsed = now - countdown_start
            remaining = COUNTDOWN_SECONDS - int(elapsed)

            if remaining > 0:
                countdown_value = remaining
            else:
                countdown_value = None
                user_gesture = detected_gesture

                if user_gesture in ["rock", "paper", "scissors"]:
                    machine_move = get_machine_move()
                    result = get_round_result(user_gesture, machine_move)
                    game.update_score(result)

                    if result == "user":
                        result_text = f"{username} wins the round!"
                        say_user_scores(username)
                    elif result == "machine":
                        result_text = "Machine wins the round!"
                        say_machine_scores()
                    else:
                        result_text = "It's a Draw!"
                        say_draw()
                else:
                    result_text = "No valid gesture! Try again."

                countdown_start = None
                result_display_start = now
                round_active = False

        # Show result then move to next round
        if result_display_start is not None:
            if now - result_display_start >= RESULT_DISPLAY_TIME:
                result_display_start = None
                if game.is_game_over():
                    break
                round_active = True

        # Update GUI
        gui.update_frame(frame)
        gui.update_scores(game.user_score, game.machine_score)
        gui.update_moves(user_gesture, machine_move)
        gui.update_countdown(countdown_value)
        gui.update_result(result_text)

        gui.root.update()

    # Game over
    winner = game.get_winner()
    if winner == "user":
        say_user_wins(username)
        gui.update_result(f"🎉 {username} wins the game!")
    elif winner == "machine":
        say_machine_wins()
        gui.update_result("🤖 Machine wins the game!")

    gui.root.update()
    time.sleep(3)
    cap.release()
    gui.root.destroy()

def main():
    import sys as _sys
    if len(_sys.argv) > 1:
        username = _sys.argv[1].strip() or "Player"
    else:
        username = input("Enter your name: ").strip()
        if not username:
            username = "Player"

    gui = GameGUI(username)

    game_thread = threading.Thread(target=run_game, args=(username, gui))
    game_thread.daemon = True
    game_thread.start()

    gui.start()

if __name__ == "__main__":
    main()