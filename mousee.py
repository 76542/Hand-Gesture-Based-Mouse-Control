import cv2
import mediapipe as mp
import pyautogui
import random
import utility as util
from pynput.mouse import Button, Controller

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

def find_finger_tip(processed):
    if processed.multi_hand_landmarks:
        hand_landmarks = processed.multi_hand_landmarks[0]  #assuming only one hand is detected
        index_finger_tip = hand_landmarks.landmark[mpHands.HandLandmark.INDEX_FINGER_TIP]
        return index_finger_tip
    return None

def move_mouse(index_finger_tip):
    if index_finger_tip is not None:
        x = int(index_finger_tip.x * screen_width)
        y = int(index_finger_tip.y * screen_height)

        smoothing_factor = 0.3  
        movement_threshold = 2  #reduced threshold for more sensitivity

        if not hasattr(move_mouse, "prev_x"):
            move_mouse.prev_x, move_mouse.prev_y = x, y

        #calculating new position with smoothing
        new_x = int(move_mouse.prev_x + (x - move_mouse.prev_x) * smoothing_factor)
        new_y = int(move_mouse.prev_y + (y - move_mouse.prev_y) * smoothing_factor)

        #moving mouse only if it exceeds the movement threshold
        if abs(new_x - move_mouse.prev_x) > movement_threshold or abs(new_y - move_mouse.prev_y) > movement_threshold:
            pyautogui.moveTo(new_x, new_y)

        #update previous position
        move_mouse.prev_x, move_mouse.prev_y = new_x, new_y

def is_left_click(landmark_list, thumb_angle):
    #index finger bent, middle finger extended
    index_angle = util.get_angle(landmark_list[5], landmark_list[6], landmark_list[8])
    middle_angle = util.get_angle(landmark_list[9], landmark_list[10], landmark_list[12])
    
    return (index_angle < 30 and middle_angle > 60)      

def is_right_click(landmark_list, thumb_angle):
    #middle finger bent, index finger extended
    index_angle = util.get_angle(landmark_list[5], landmark_list[6], landmark_list[8])
    middle_angle = util.get_angle(landmark_list[9], landmark_list[10], landmark_list[12])
    
    return (middle_angle < 30 and index_angle > 60)       

def is_double_click(landmark_list, thumb_angle):
    #both index and middle fingers extended
    index_angle = util.get_angle(landmark_list[5], landmark_list[6], landmark_list[8])
    middle_angle = util.get_angle(landmark_list[9], landmark_list[10], landmark_list[12])
    
    return (index_angle < 30 and    # Index finger is extended
            middle_angle < 30)      # Middle finger is extended

def is_screenshot(landmark_list, thumb_angle):
    #all fingers closed (fist)
    index_angle = util.get_angle(landmark_list[5], landmark_list[6], landmark_list[8])
    middle_angle = util.get_angle(landmark_list[9], landmark_list[10], landmark_list[12])
    ring_angle = util.get_angle(landmark_list[13], landmark_list[14], landmark_list[16])
    
    return (index_angle > 60 and    #index finger is bent
            middle_angle > 60 and   #middle finger is bent
            ring_angle > 60)        #ring finger is bent

def detect_gesture(frame, landmark_list, processed):
    if len(landmark_list) >= 21:
        index_finger_tip = find_finger_tip(processed)
        
        #calculate angles for fingers
        thumb_angle = util.get_angle(landmark_list[1], landmark_list[2], landmark_list[4])
        index_angle = util.get_angle(landmark_list[5], landmark_list[6], landmark_list[8])
        middle_angle = util.get_angle(landmark_list[9], landmark_list[10], landmark_list[12])
        
        #large angle indicates extended thumb)
        is_thumb_extended = thumb_angle > 170
        
        #debugging info
        cv2.putText(frame, f"Thumb angle: {thumb_angle:.1f}", 
                   (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
        
        #mouse movement happens when thumb is NOT EXTENDED (closed against palm)
        if not is_thumb_extended:
            move_mouse(index_finger_tip)
            cv2.putText(frame, "Mouse Moving", (50, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
        else:
            cv2.putText(frame, "Mouse Locked", (50, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)
            
            #checking for gestures when mouse is stopped
            if is_left_click(landmark_list, thumb_angle):
                mouse.press(Button.left)
                mouse.release(Button.left)
                cv2.putText(frame, "Left Click", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
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
                im1 = pyautogui.screenshot()
                label = random.randint(1, 1000)
                im1.save(f'my_screenshot_{label}.png')
                cv2.putText(frame, "Screenshot Taken", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
                pyautogui.sleep(1.0)

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
                hand_landmarks = processed.multi_hand_landmarks[0]  #assuming only one hand is detected
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