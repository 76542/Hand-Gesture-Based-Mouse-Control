import cv2
import mediapipe as mp
import pyautogui
import random
import utility as util
import time
from pynput.mouse import Button, Controller
import numpy as np

mouse = Controller()
screen_width, screen_height = pyautogui.size()

mpHands = mp.solutions.hands
hands = mpHands.Hands(
    static_image_mode=False,
    model_complexity=1,
    min_detection_confidence=0.9,  
    min_tracking_confidence=0.9,     
    max_num_hands=1
)

last_screenshot_time=0  # Initialize last screenshot time

def find_finger_tip(processed):
    if processed.multi_hand_landmarks:
        hand_landmarks = processed.multi_hand_landmarks[0]
        index_finger_tip = hand_landmarks.landmark[mpHands.HandLandmark.INDEX_FINGER_TIP]
        return index_finger_tip
    return None

def move_mouse(index_finger_tip):
    if index_finger_tip is not None:
        x = int(index_finger_tip.x * screen_width)
        y = int(index_finger_tip.y * screen_height)

        smoothing_factor = 0.3
        movement_threshold = 2

        if not hasattr(move_mouse, "prev_x"):
            move_mouse.prev_x, move_mouse.prev_y = x, y

        new_x = int(move_mouse.prev_x + (x - move_mouse.prev_x) * smoothing_factor)
        new_y = int(move_mouse.prev_y + (y - move_mouse.prev_y) * smoothing_factor)

        if abs(new_x - move_mouse.prev_x) > movement_threshold or abs(new_y - move_mouse.prev_y) > movement_threshold:
            pyautogui.moveTo(new_x, new_y)

        move_mouse.prev_x, move_mouse.prev_y = new_x, new_y

def is_scroll_gesture(landmark_list):
    middle_angle = util.get_angle(landmark_list[9], landmark_list[10], landmark_list[12])
    ring_angle = util.get_angle(landmark_list[13], landmark_list[14], landmark_list[16])
    index_angle = util.get_angle(landmark_list[5], landmark_list[6], landmark_list[8])
    pinky_angle = util.get_angle(landmark_list[17], landmark_list[18], landmark_list[20])

    print(f"Scroll Gesture Angles -> Middle: {middle_angle:.2f}, Ring: {ring_angle:.2f}, Index: {index_angle:.2f}, Pinky: {pinky_angle:.2f}")

    return (
    middle_angle < 180 and
    ring_angle < 50 and
    index_angle > 40 and
    pinky_angle > 40
)

def get_scroll_amount(landmark_list):
    wrist_y = landmark_list[0][1]
    middle_tip_y = landmark_list[12][1]

    if not hasattr(get_scroll_amount, "prev_y"):
        get_scroll_amount.prev_y = middle_tip_y

    dy = middle_tip_y - get_scroll_amount.prev_y
    get_scroll_amount.prev_y = middle_tip_y

    scroll_speed = 3000  # Increased sensitivity for debugging
    scroll_amount = int(-dy * scroll_speed)

    print(f"Scroll delta: {dy:.5f}, Scroll amount: {scroll_amount}")
    return scroll_amount

def is_left_click(landmark_list, thumb_angle):
    index_angle = util.get_angle(landmark_list[5], landmark_list[6], landmark_list[8])
    middle_angle = util.get_angle(landmark_list[9], landmark_list[10], landmark_list[12])

    print(f"Left Click Angles -> Index: {index_angle:.1f}, Middle: {middle_angle:.1f}, Thumb: {thumb_angle:.1f}")

    return (
        thumb_angle > 170 and   
        index_angle < 30 and    
        middle_angle > 60       
    )

def is_right_click(landmark_list, thumb_angle):
    index_angle = util.get_angle(landmark_list[5], landmark_list[6], landmark_list[8])
    middle_angle = util.get_angle(landmark_list[9], landmark_list[10], landmark_list[12])

    print(f"Right Click Angles -> Index: {index_angle:.1f}, Middle: {middle_angle:.1f}, Thumb: {thumb_angle:.1f}")

    return (
        thumb_angle > 170 and     # Thumb extended(mouse locked)
        index_angle > 60 and      # Index extended
        middle_angle < 30         # Middle bent
    )


def is_double_click(landmark_list, thumb_angle):
    index_angle = util.get_angle(landmark_list[5], landmark_list[6], landmark_list[8])
    middle_angle = util.get_angle(landmark_list[9], landmark_list[10], landmark_list[12])
    return (index_angle < 30 and middle_angle < 30)

def is_screenshot(landmark_list, thumb_angle):
    index_angle = util.get_angle(landmark_list[5], landmark_list[6], landmark_list[8])
    middle_angle = util.get_angle(landmark_list[9], landmark_list[10], landmark_list[12])
    ring_angle = util.get_angle(landmark_list[13], landmark_list[14], landmark_list[16])
    pinky_angle = util.get_angle(landmark_list[17], landmark_list[18], landmark_list[20])

    index_bent = index_angle < 90
    middle_bent = middle_angle < 90
    ring_bent = ring_angle < 90
    pinky_bent = pinky_angle < 90
    thumb_extended = thumb_angle > 150


    return (
        index_bent and
        middle_bent and
        ring_bent and
        pinky_bent and
        thumb_extended
    )
       


def is_zoom_gesture(landmarks):
    thumb_tip = landmarks[4]
    index_tip = landmarks[8]
    middle_angle = util.get_angle(landmarks[9], landmarks[10], landmarks[12])
    thumb_angle = util.get_angle(landmarks[1], landmarks[2], landmarks[4])

    pinch_distance = np.hypot(index_tip[0] - thumb_tip[0], index_tip[1] - thumb_tip[1])

    
    if thumb_angle < 170 or middle_angle < 50:
        return False

    if not hasattr(is_zoom_gesture, "prev_distance"):
        is_zoom_gesture.prev_distance = pinch_distance

    diff = pinch_distance - is_zoom_gesture.prev_distance
    is_zoom_gesture.prev_distance = pinch_distance

    print(f"Zoom Pinch -> Thumb angle: {thumb_angle:.1f}, Middle angle: {middle_angle:.1f}, Pinch diff: {diff:.4f}")

    return abs(diff) > 0.005 and pinch_distance < 0.1



def get_zoom_factor(landmarks):
    thumb_tip = landmarks[4]
    index_tip = landmarks[8]
    distance = np.hypot(index_tip[0] - thumb_tip[0], index_tip[1] - thumb_tip[1])

    if not hasattr(get_zoom_factor, "prev_distance"):
        get_zoom_factor.prev_distance = distance
        return 0

    factor = distance - get_zoom_factor.prev_distance
    get_zoom_factor.prev_distance = distance

    return factor

def detect_gesture(frame, landmark_list, processed):
    if len(landmark_list) >= 21:
        index_finger_tip = find_finger_tip(processed)
        thumb_angle = util.get_angle(landmark_list[1], landmark_list[2], landmark_list[4])
        index_angle = util.get_angle(landmark_list[5], landmark_list[6], landmark_list[8])
        middle_angle = util.get_angle(landmark_list[9], landmark_list[10], landmark_list[12])
        is_thumb_extended = thumb_angle > 170

        cv2.putText(frame, f"Thumb angle: {thumb_angle:.1f}", 
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

        if not is_thumb_extended:
            move_mouse(index_finger_tip)
            cv2.putText(frame, "Mouse Moving", (50, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
        else:
            cv2.putText(frame, "Mouse Locked", (50, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)

            if is_scroll_gesture(landmark_list):
                scroll_amount = get_scroll_amount(landmark_list)
                pyautogui.scroll(scroll_amount)
                cv2.putText(frame, f"Scrolling: {scroll_amount}", 
                            (50, 110), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            elif is_zoom_gesture(landmark_list):
                zoom_factor = get_zoom_factor(landmark_list)
                if zoom_factor > 0:
                    pyautogui.keyDown('ctrl')
                    pyautogui.press('=')
                    pyautogui.keyUp('ctrl')
                    cv2.putText(frame, "Zooming In", (50, 140), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 165, 0), 2)
                elif zoom_factor < 0:
                    pyautogui.keyDown('ctrl')
                    pyautogui.press('-')
                    pyautogui.keyUp('ctrl')
                    cv2.putText(frame, "Zooming Out", (50, 140), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 165, 0), 2)

            elif is_left_click(landmark_list, thumb_angle):
                mouse.press(Button.left)
                mouse.release(Button.left)
                cv2.putText(frame, "Left Click", (50, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                pyautogui.sleep(0.3)
            elif is_right_click(landmark_list, thumb_angle):
                mouse.press(Button.right)
                mouse.release(Button.right)
                cv2.putText(frame, "Right Click", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                pyautogui.sleep(0.3)
            elif is_double_click(landmark_list, thumb_angle):
                pyautogui.doubleClick()
                cv2.putText(frame, "Double Click", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
                pyautogui.sleep(0.5)
            elif is_screenshot(landmark_list, thumb_angle):
                global last_screenshot_time  # Let us modify the global variable
                current_time = time.time()
                if current_time - last_screenshot_time > 2:  # 2-second cooldown
                    im1 = pyautogui.screenshot()
                    label = random.randint(1, 1000)
                    im1.save(f'my_screenshot_{label}.png')
                    cv2.putText(frame, "Screenshot Taken", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
                    last_screenshot_time = current_time


def main():
    draw = mp.solutions.drawing_utils
    cap = cv2.VideoCapture(0)

    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            frame = cv2.flip(frame, 1)
            frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            processed = hands.process(frameRGB)

            landmark_list = []
            if processed.multi_hand_landmarks:
                hand_landmarks = processed.multi_hand_landmarks[0]
                draw.draw_landmarks(frame, hand_landmarks, mpHands.HAND_CONNECTIONS)
                for lm in hand_landmarks.landmark:
                    landmark_list.append((lm.x, lm.y))

            detect_gesture(frame, landmark_list, processed)

            cv2.imshow('Frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
