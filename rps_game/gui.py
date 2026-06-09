import tkinter as tk
from PIL import Image, ImageTk
import cv2

class GameGUI:
    def __init__(self, username):
        self.username = username
        self.root = tk.Tk()
        self.root.title("Rock Paper Scissors")
        self.root.configure(bg="#1a1a2e")
        self.root.resizable(False, False)

        # Title
        tk.Label(self.root, text="✊ Rock Paper Scissors ✋",
                 font=("Arial", 20, "bold"), bg="#1a1a2e", fg="#e94560").pack(pady=10)

        # Webcam feed
        self.video_label = tk.Label(self.root, bg="#1a1a2e")
        self.video_label.pack()

        # Score frame
        score_frame = tk.Frame(self.root, bg="#1a1a2e")
        score_frame.pack(pady=10)

        tk.Label(score_frame, text=f"{username}:", font=("Arial", 14, "bold"),
                 bg="#1a1a2e", fg="#0f3460").grid(row=0, column=0, padx=20)
        self.user_score_label = tk.Label(score_frame, text="0",
                 font=("Arial", 24, "bold"), bg="#1a1a2e", fg="#00ff88")
        self.user_score_label.grid(row=0, column=1, padx=5)

        tk.Label(score_frame, text="Machine:", font=("Arial", 14, "bold"),
                 bg="#1a1a2e", fg="#0f3460").grid(row=0, column=2, padx=20)
        self.machine_score_label = tk.Label(score_frame, text="0",
                 font=("Arial", 24, "bold"), bg="#1a1a2e", fg="#ff4444")
        self.machine_score_label.grid(row=0, column=3, padx=5)

        # Move frame
        move_frame = tk.Frame(self.root, bg="#1a1a2e")
        move_frame.pack(pady=5)

        tk.Label(move_frame, text="Your Move:", font=("Arial", 12),
                 bg="#1a1a2e", fg="#ffffff").grid(row=0, column=0, padx=15)
        self.user_move_label = tk.Label(move_frame, text="-",
                 font=("Arial", 14, "bold"), bg="#1a1a2e", fg="#00ff88")
        self.user_move_label.grid(row=0, column=1, padx=5)

        tk.Label(move_frame, text="Machine Move:", font=("Arial", 12),
                 bg="#1a1a2e", fg="#ffffff").grid(row=0, column=2, padx=15)
        self.machine_move_label = tk.Label(move_frame, text="-",
                 font=("Arial", 14, "bold"), bg="#1a1a2e", fg="#ff4444")
        self.machine_move_label.grid(row=0, column=3, padx=5)

        # Countdown label
        self.countdown_label = tk.Label(self.root, text="",
                 font=("Arial", 48, "bold"), bg="#1a1a2e", fg="#00ccff")
        self.countdown_label.pack()

        # Result label
        self.result_label = tk.Label(self.root, text="",
                 font=("Arial", 16, "bold"), bg="#1a1a2e", fg="#ffffff")
        self.result_label.pack(pady=10)

    def update_frame(self, frame):
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame_rgb)
        img = img.resize((640, 400))
        imgtk = ImageTk.PhotoImage(image=img)
        self.video_label.imgtk = imgtk
        self.video_label.configure(image=imgtk)

    def update_scores(self, user_score, machine_score):
        self.user_score_label.config(text=str(user_score))
        self.machine_score_label.config(text=str(machine_score))

    def update_moves(self, user_move, machine_move):
        self.user_move_label.config(text=user_move)
        self.machine_move_label.config(text=machine_move)

    def update_countdown(self, value):
        self.countdown_label.config(text=str(value) if value else "")

    def update_result(self, text):
        self.result_label.config(text=text if text else "")

    def start(self):
        self.root.mainloop()