# Hand-Gesture-Based-Mouse-Control

This project is a hand gesture recognition system that allows users to control the mouse using hand gestures detected through a webcam. The system uses **Mediapipe**, **OpenCV**, and **PyAutoGUI** to automate mouse movements, clicks, and perform actions like screenshots based on hand gestures.

## Features
- **Mouse Movement**: Move the mouse cursor by simply moving your hand in front of the camera.
- **Left Click**: Make a left-click gesture by bending your index finger and extending your middle finger.
- **Right Click**: Perform a right-click gesture by bending your middle finger and extending your index finger.
- **Double Click**: Perform a double-click gesture by extending both your index and middle fingers.
- **Screenshot**: Take a screenshot by making a fist gesture (all fingers bent).

## Requirements
- Python 3.x
- OpenCV
- Mediapipe
- PyAutoGUI
- Pynput
- Numpy

Install the required libraries using pip:

```bash
pip install opencv-python mediapipe pyautogui pynput numpy
