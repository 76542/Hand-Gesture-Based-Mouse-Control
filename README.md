# 🖐️ Hand Gesture-Based Mouse Control

A real-time computer vision system that allows users to control the mouse cursor and perform common mouse actions using hand gestures detected through a standard webcam. This project uses **MediaPipe**, **OpenCV**, and **PyAutoGUI** to enable contactless, gesture-driven interaction.

---

## ✨ Features

| **Gesture**        | **Functionality**                                                   |
|--------------------|----------------------------------------------------------------------|
| 🖱️ **Cursor Movement** | Move the mouse using the index fingertip (thumb bent = active control) |
| 👆 **Left Click**        | Bend the index finger, extend middle & thumb to left-click         |
| 👉 **Right Click**       | Bend the middle finger, extend index & thumb to right-click        |
| 👇 **Double Click**      | Bend both index and middle fingers simultaneously                  |
| 🔃 **Scroll**            | Bend middle and ring fingers; move hand up/down to scroll vertically |
| 🔍 **Zoom**              | Perform a pinch gesture (index-thumb), and adjust distance to zoom in/out |
| 📸 **Screenshot**        | All fingers bent, thumb extended — captures screenshot (with cooldown) |

Each gesture is angle-based and robust to lighting variations, with real-time on-screen feedback and smooth interaction.

---

## 🧠 How It Works

- Uses **MediaPipe** to track 21 hand landmarks.
- Calculates **joint angles** using a custom geometric approach.
- Classifies gestures with a **rule-based engine** (no ML model required).
- Executes system-level actions using **pyautogui** and **pynput**.
- Built-in **gesture prioritization** and **cooldown logic** avoid conflicts.

---

## 🖥️ Requirements

- Python 3.9+
- Webcam (720p or better recommended)

### Install Dependencies:

```bash
pip install opencv-python mediapipe pyautogui pynput numpy
