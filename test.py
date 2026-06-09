import cv2
import mediapipe as mp
import pyttsx3

print("OpenCV version:", cv2.__version__)
print("MediaPipe imported successfully")

engine = pyttsx3.init()
engine.say("Environment setup complete")
engine.runAndWait()
print("pyttsx3 working")
