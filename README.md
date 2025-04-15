# 🖐️ Hand Gesture-Based Mouse Control System

A real-time gesture recognition system that transforms your webcam into a contactless input device — enabling you to control your mouse using only your hand. Built with **MediaPipe**, **OpenCV**, and **PyAutoGUI**, this project interprets hand landmarks into intuitive mouse actions including movement, clicks, scrolling, zoom, and screenshot capture.

---

## 🚀 Project Overview

This system tracks a user’s hand using a webcam and interprets gestures by analyzing the angles between key joints on the fingers. Unlike machine learning models, this rule-based approach doesn't require training data, making it lightweight, fast, and user-independent.

---

## ✅ Key Features

| Feature           | Description                                                                 |
|------------------|-----------------------------------------------------------------------------|
| 🖱️ Mouse Movement | Move cursor using the index finger when thumb is bent (gesture unlocked)     |
| 👆 Left Click     | Thumb extended, index finger bent, middle extended                          |
| 👉 Right Click    | Thumb extended, index extended, middle bent                                 |
| ✌️ Double Click   | Both index and middle fingers bent simultaneously                          |
| 🔃 Scroll         | Middle and ring fingers bent, index and pinky extended; scroll on motion    |
| 🔍 Zoom In/Out    | Pinch gesture between thumb and index finger with dynamic distance tracking |
| 📸 Screenshot     | All fingers bent, thumb extended — with 2-second cooldown                   |
| 🔒 Gesture Lock   | Thumb extended locks mouse movement to avoid unintended control             |
| 🧠 Visual Feedback| Real-time overlays for detected gesture, angles, and action status          |

---

## 🧰 Tech Stack

- **Language**: Python 3.9  
- **Hand Tracking**: [MediaPipe Hands](https://google.github.io/mediapipe/solutions/hands.html)  
- **Computer Vision**: [OpenCV](https://opencv.org/)  
- **Mouse/Keyboard Automation**: [PyAutoGUI](https://pyautogui.readthedocs.io)  
- **Low-Level Control**: [pynput](https://pynput.readthedocs.io)  
- **Math Utilities**: NumPy  
- **Custom Logic**: `utility.py` — computes joint angles for gesture recognition  

---

## 📦 Installation

Install all dependencies:

```bash
pip install opencv-python mediapipe pyautogui pynput numpy

🧪 How to Run
Clone the repository:

bash
Copy
Edit
git clone https://github.com/yourusername/Hand-Gesture-Based-Mouse-Control.git
cd Hand-Gesture-Based-Mouse-Control
Run the main script:

bash
Copy
Edit
python mousee.py
Press q to exit.

Make sure your webcam is active and your hand is 30–60 cm away from the camera in a well-lit environment.

📂 Project Structure
bash
Copy
Edit
├── mousee.py           # Main gesture detection and control logic
├── utility.py          # Angle computation functions
├── requirements.txt    # Project dependencies
├── README.md           # Project documentation
└── screenshots/        # (Optional) Captured screenshots
📸 Demonstration
Add labeled gesture screenshots or GIF demos here:

🖱️ Cursor Movement

👆 Left Click

🔍 Zoom In/Out

🔃 Scroll

📸 Screenshot Capture

