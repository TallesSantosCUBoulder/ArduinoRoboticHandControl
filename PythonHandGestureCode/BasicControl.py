# This code detects whether fingers are up or down using MediaPipe hand landmarks.
# MediaPipe provides 21 landmark points for each hand, including fingertips and joints.

# For the index, middle, ring, and pinky fingers, the code compares the y-coordinate
# of the fingertip with the y-coordinate of the joint below it. If the fingertip is
# higher (smaller y value in image coordinates), the finger is considered "up";
# otherwise it is "down".

# The thumb is handled differently because it moves sideways instead of vertically.
# So the code compares x-coordinates instead of y-coordinates, and adjusts the logic
# depending on whether the detected hand is left or right.

# Additionally, the code measures the distance between the thumb tip and index tip
# to detect a pinch gesture (like an "OK" sign), normalized by hand size for stability.

# Finally, these individual finger states (True/False values) are combined to recognize
# specific hand gestures such as fist, peace sign, five fingers, or other custom gestures.

import serial
import time
import cv2
import mediapipe as mp
import math

arduino = serial.Serial(port='/dev/cu.usbmodem14101', baudrate=115200, timeout=.1)

def write_read(x):
    arduino.write(bytes(str(x), 'utf-8'))
    time.sleep(0.05)
    data = arduino.readline()
    return data

# MediaPipe setup
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

cam = cv2.VideoCapture(0)

last_sent = None

def distance(p1, p2, w, h):
    x1, y1 = int(p1.x * w), int(p1.y * h)
    x2, y2 = int(p2.x * w), int(p2.y * h)
    return math.hypot(x2 - x1, y2 - y1)

def recognize_gesture(hand_landmarks, label, w, h):
    lm = hand_landmarks.landmark

    index_up = lm[8].y < lm[6].y
    middle_up = lm[12].y < lm[10].y
    ring_up = lm[16].y < lm[14].y
    pinky_up = lm[20].y < lm[18].y

    if label == "Right":
        thumb_up = lm[4].x < lm[3].x
    else:
        thumb_up = lm[4].x > lm[3].x

    pinch_distance = distance(lm[4], lm[8], w, h)
    hand_size = distance(lm[0], lm[9], w, h)

    if hand_size > 0:
        pinch_ratio = pinch_distance / hand_size
    else:
        pinch_ratio = 1

    thumb_index_pinch = pinch_ratio < 0.35

    if thumb_index_pinch and middle_up and ring_up and pinky_up:
        return 8, "Gesture 8: OK"

    if thumb_up and index_up and not middle_up and not ring_up and pinky_up:
        return 7, "Gesture 7: Love You"

    if thumb_up and not index_up and not middle_up and not ring_up and pinky_up:
        return 6, "Gesture 6: Hang Loose"

    if not thumb_up and not index_up and middle_up and not ring_up and not pinky_up:
        return 9, "Gesture 9: Middle Finger"

    if thumb_up and index_up and middle_up and ring_up and pinky_up:
        return 5, "Gesture 5: Five / Open Hand"

    if not thumb_up and index_up and middle_up and ring_up and pinky_up:
        return 4, "Gesture 4: Four"

    if not thumb_up and index_up and middle_up and ring_up and not pinky_up:
        return 3, "Gesture 3: Three"

    if not thumb_up and index_up and middle_up and not ring_up and not pinky_up:
        return 2, "Gesture 2: Two / Peace"

    if not thumb_up and index_up and not middle_up and not ring_up and not pinky_up:
        return 1, "Gesture 1: One"

    if not thumb_up and not index_up and not middle_up and not ring_up and not pinky_up:
        return 0, "Default: Fist"

    return None, "Unknown Gesture"

# Main loop
while True:
    success, img = cam.read()
    if not success:
        break

    img = cv2.flip(img, 1)
    h, w, _ = img.shape

    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    if results.multi_hand_landmarks and results.multi_handedness:
        hand_landmarks = results.multi_hand_landmarks[0]
        handedness = results.multi_handedness[0]
        label = handedness.classification[0].label

        if label == "Right":

            mp_draw.draw_landmarks(
                img,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

            gesture_number, gesture_text = recognize_gesture(hand_landmarks, label, w, h)

            if gesture_number is not None and gesture_number != last_sent:
                value = write_read(gesture_number)
                print(value)
                last_sent = gesture_number

            cv2.putText(
                img,
                "Keep Palm Facing The Camera",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 0, 255),
                2
            )

            cv2.putText(
                img,
                gesture_text,
                (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2
            )

            cv2.putText(
                img,
                f"Sending: {gesture_number}",
                (20, 120),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255, 255, 0),
                2
            )

        else:
            cv2.putText(
                img,
                "Show Right Hand Only",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 0, 255),
                2
            )
            last_sent = None

    else:
        cv2.putText(
            img,
            "No Hand Detected",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 0, 255),
            2
        )
        last_sent = None

    cv2.imshow("Hand Volume Control", img)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Cleanup
cam.release()
cv2.destroyAllWindows()
arduino.close()