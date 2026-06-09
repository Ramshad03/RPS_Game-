import subprocess
import threading

def _speak(text):
    cmd = f'Add-Type -AssemblyName System.Speech; $s = New-Object System.Speech.Synthesis.SpeechSynthesizer; $s.Rate = 1; $s.Speak("{text}")'
    subprocess.run(["powershell", "-Command", cmd],
                  capture_output=True, creationflags=0x08000000)

def speak(text):
    thread = threading.Thread(target=_speak, args=(text,), daemon=True)
    thread.start()

def speak_and_wait(text):
    thread = threading.Thread(target=_speak, args=(text,), daemon=True)
    thread.start()
    thread.join()

def say_welcome(username):
    speak_and_wait(f"Welcome {username}")

def say_game_start(username):
    speak_and_wait(f"Lets start the game {username}")

def say_user_scores(username):
    speak(f"{username} scores 1 point")

def say_machine_scores():
    speak("I score 1 point")

def say_draw():
    speak("Its a draw")

def say_user_wins(username):
    speak_and_wait(f"Congratulations {username}, you win the game")

def say_machine_wins():
    speak_and_wait("I win the game")

def say_countdown(number):
    speak(str(number))