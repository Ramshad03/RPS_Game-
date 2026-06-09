# Robot Assistant

An intelligent robot assistant with real-time face recognition, animal detection, voice interaction, and an AI-powered conversational brain.

---

## Features

- **Face Recognition** — identifies known people from the camera; prompts unknowns to register with a multi-angle face scan
- **Animal Detection** — detects animals via YOLOv8 and lets you name them for future recognition
- **Voice Interaction** — listens via microphone (SpeechRecognition + PyAudio) and speaks responses (pyttsx3)
- **AI Brain** — powered by Groq's LLaMA 3.3 70B; remembers personal facts users share across sessions
- **Vision Mode** — send the live camera frame to Groq Vision for scene description
- **Rock Paper Scissors Game** — trigger a full RPS game by voice
- **Live Display** — on-screen overlay showing camera feed, detected faces/animals, and robot status
- **Persistent Memory** — conversation history and learned user facts stored locally in SQLite

---

## Project Structure

```
ROBOT MAIN/
├── main.py                  # Entry point — robot loop, identification flow, AI brain
├── vision_pipeline.py       # Camera feed & Groq Vision integration
├── display.py               # On-screen display overlay
├── requirements.txt         # Python dependencies
├── start_robot.bat          # Windows launch script
├── yolov8n.pt               # YOLOv8 nano model weights
├── face_landmarker.task     # MediaPipe face landmarker model
├── modules/
│   ├── face_recognition_module.py   # dlib-based face recognition
│   ├── animal_recognition_module.py # MobileNetV2 animal classifier
│   ├── voice_module.py              # TTS + STT, barge-in control
│   ├── voice_interaction.py         # High-level voice helpers
│   ├── vad_module.py                # Voice Activity Detection
│   ├── lip_detector.py              # MediaPipe lip movement detection
│   ├── rps_module.py                # Rock Paper Scissors game
│   └── database.py                  # SQLite persistence layer
├── data/                    # Registered face encodings
└── local_data/              # SQLite database files
```

---

## Requirements

- Python **3.9 – 3.11** (3.11 recommended; `tensorflow-cpu==2.21.0` does not support 3.12+)
- Windows 10/11 (pyttsx3 uses the Windows SAPI5 voice engine)
- A webcam
- A microphone
- A [Groq API key](https://console.groq.com)

---

## How to Run (step-by-step)

### Step 1 — Install Visual Studio Build Tools (required for `dlib`)

`dlib` must be compiled from source on Windows. Without this step, `pip install dlib` will fail.

1. Download **Visual Studio Build Tools** from [visualstudio.microsoft.com/visual-cpp-build-tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
2. Run the installer and select **"Desktop development with C++"**
3. Complete the installation and restart your PC if prompted

> **Alternative:** Install a pre-built `dlib` wheel instead of compiling:
> ```
> pip install https://github.com/jloh02/dlib/releases/download/v19.22/dlib-19.22.99-cp311-cp311-win_amd64.whl
> ```
> (Replace `cp311` with your Python version, e.g. `cp39` for Python 3.9)

---

### Step 2 — Clone / download the project

If you downloaded a ZIP, extract it. Then open a terminal in the project folder:

```
cd "path\to\ROBOT MAIN"
```

---

### Step 3 — (Recommended) Create a virtual environment

```
python -m venv venv
venv\Scripts\activate
```

Your prompt should now show `(venv)`.

---

### Step 4 — Install dependencies

```
pip install -r requirements.txt
```

This installs all required packages across these categories:

| Category | Key packages |
|---|---|
| AI Brain | `groq` |
| Environment | `python-dotenv` |
| Computer Vision | `opencv-python`, `mediapipe` |
| Voice Input | `SpeechRecognition`, `pyaudio`, `openai-whisper`, `webrtcvad`, `noisereduce` |
| Voice Output | `pyttsx3` |
| Deep Learning | `torch`, `torchvision` |
| Face Recognition | `face_recognition`, `deepface`, `tensorflow-cpu==2.21.0`, `cmake`, `dlib` |
| Object Detection | `ultralytics` (YOLOv8) |
| Utilities | `numpy`, `Pillow` |

> **PyAudio on Windows:** If `pyaudio` fails to install, download the matching `.whl` from [PyPI](https://pypi.org/project/PyAudio/#files) or run:
> ```
> pip install pipwin && pipwin install pyaudio
> ```

---

### Step 5 — Add your Groq API key

Create a file named `.env` in the project root (same folder as `main.py`):

```env
GROQ_API_KEY=your_groq_api_key_here
CAMERA_INDEX=0
```

- Get a free API key at [console.groq.com](https://console.groq.com)
- `CAMERA_INDEX=0` uses the first detected webcam (change to `1`, `2`, etc. if needed)

---

### Step 6 — Verify model files are present

Confirm the following files exist in the project root:

```
ROBOT MAIN/
├── yolov8n.pt           ← YOLOv8 weights
└── face_landmarker.task ← MediaPipe face landmarker
```

These are not downloaded automatically. If missing, see the notes at the bottom of this file.

---

### Step 7 — Run the robot

**Option A — Double-click (easiest)**

Double-click `start_robot.bat`. A terminal opens and the robot starts automatically.

**Option B — Command line**

```
python main.py
```

---

### What happens at startup

1. **Module loading** — face recognition, animal detection, voice, and display systems initialise
2. **Camera warm-up** — ~2.5 seconds for the camera to stabilise
3. **Identification** — scans for a known face; if unknown, prompts for name registration; if no face, checks for animals
4. **Main loop** — listens continuously for voice commands

---

### Shutting down

Say **"Goodbye"**, **"Shut down"**, or **"Turn off"** — the robot saves state and exits cleanly.  
You can also press `Ctrl+C` in the terminal for an immediate stop.

---

### Troubleshooting

**Wrong camera detected**

Run the camera finder utility to list available indices:

```
python find_camera.py
```

Then update `.env`:

```env
CAMERA_INDEX=1
```

**Re-register your face**

```
python re_register_face.py
```

**Register multiple faces at once**

```
python multi_register_face.py
```

**Missing `yolov8n.pt`**

```python
from ultralytics import YOLO
YOLO("yolov8n.pt")   # downloads automatically on first run
```

**Missing `face_landmarker.task`**

Download from [MediaPipe Models](https://developers.google.com/mediapipe/solutions/vision/face_landmarker#models) and place it in the project root.

---

**`dlib` error: "Unsupported image type" on every frame**

This is a NumPy 2.x / dlib ABI incompatibility — not a Python-level bug.

| Package | Bad version | Good version |
|---|---|---|
| `numpy` | 2.x | < 2.0 |
| `dlib` | 19.24.1 | any (compiled for NumPy 1.x) |

NumPy 2.0 changed its internal C-level array layout (ABI). `dlib` was compiled against the NumPy 1.x headers, so when it receives a 2.x array it cannot read the dtype field correctly — causing the error on every single frame. No Python-level fix (`.astype()`, `np.ascontiguousarray`, `cvtColor`) works because the problem is at the binary memory layout level.

Fix — downgrade NumPy:

```
pip install "numpy<2.0"
```

This is already pinned in `requirements.txt` so a fresh `pip install -r requirements.txt` will never hit this issue.

---

## Usage

| Voice Trigger | Action |
|---|---|
| "What do you see?" / "Look at this" | Activates vision mode — describes the scene |
| "Let's play rock paper scissors" | Starts the RPS game |
| "Goodbye" / "Shut down" / "Turn off" | Cleanly shuts down the robot |
| Any other speech | Conversational AI response |

On first encounter, the robot asks for your name and performs a multi-angle face scan to register you. Subsequent sessions greet you by name automatically.

---

## How It Works

1. **Startup** — loads face/animal modules, checks camera and API key, warms up the camera
2. **Identification** — scans for a known face; if unknown, registers via voice + multi-angle scan; if no face, checks for animals
3. **Main loop** — listens continuously; background thread watches for new unknown faces/animals every 30 seconds
4. **AI responses** — user speech is sent to Groq with conversation history and known user facts injected as context; new facts mentioned by the user are extracted and saved automatically

---

## Dependencies

| Package | Purpose |
|---|---|
| `groq` | LLaMA 3.3 70B AI brain + Vision |
| `opencv-python` | Camera capture and frame processing |
| `face_recognition` + `dlib` | Face detection and recognition |
| `ultralytics` | YOLOv8 object/animal detection |
| `torch` + `torchvision` | MobileNetV2 animal classifier |
| `SpeechRecognition` + `pyaudio` | Microphone input |
| `pyttsx3` | Text-to-speech output |
| `python-dotenv` | Environment variable loading |
| `numpy` + `Pillow` | Image utilities |
