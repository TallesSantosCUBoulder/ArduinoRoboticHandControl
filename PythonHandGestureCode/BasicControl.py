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

import serial       # Imports the pyserial library for communicating with the Arduino over USB
import time         # Imports the time module for adding delays
import cv2          # Imports OpenCV for capturing and displaying video frames
import mediapipe as mp  # Imports MediaPipe for hand landmark detection
import math         # Imports the math module for calculating distances

# Opens a serial connection to the Arduino on the specified port at 115200 baud rate
arduino = serial.Serial(port='/dev/cu.usbmodem14301', baudrate=115200, timeout=.1)

def write_read(x):
    arduino.write(bytes(str(x), 'utf-8'))  # Converts the value x to a UTF-8 byte string and sends it to the Arduino
    time.sleep(0.05)                        # Waits 50 milliseconds to give the Arduino time to process and respond
    data = arduino.readline()              # Reads one line of response from the Arduino
    return data                            # Returns the response data from the Arduino

# Accesses the MediaPipe hand tracking solution module
mp_hands = mp.solutions.hands
# Accesses MediaPipe's built-in drawing utility for rendering landmarks on frames
mp_draw = mp.solutions.drawing_utils

# Creates a Hands object with configuration for real-time single-hand detection
hands = mp_hands.Hands(
    static_image_mode=False,        # Enables video mode (tracking across frames) instead of treating each frame independently
    max_num_hands=1,                # Limits detection to a maximum of one hand at a time
    model_complexity=0,             # Uses the lightest/fastest model (0 = lite, 1 = full)
    min_detection_confidence=0.5,   # Minimum confidence score required to consider a hand detection valid
    min_tracking_confidence=0.5     # Minimum confidence score required to keep tracking a hand between frames
)

cam = cv2.VideoCapture(0)  # Opens the default webcam (device index 0) for capturing video frames

last_sent = None  # Tracks the last gesture number sent to the Arduino to avoid sending duplicate commands

def distance(p1, p2, w, h):
    # Converts the landmark's normalized x coordinate to pixel coordinates by multiplying by frame width
    x1, y1 = int(p1.x * w), int(p1.y * h)  # Converts landmark p1 from normalized (0–1) to pixel coordinates
    x2, y2 = int(p2.x * w), int(p2.y * h)  # Converts landmark p2 from normalized (0–1) to pixel coordinates
    return math.hypot(x2 - x1, y2 - y1)    # Returns the Euclidean distance between the two pixel points

def recognize_gesture(hand_landmarks, label, w, h):
    lm = hand_landmarks.landmark  # Creates a shorthand reference to the list of 21 hand landmark points

    # Checks if the index fingertip (8) is above its lower joint (6) in image coordinates (smaller y = higher on screen)
    index_up = lm[8].y < lm[6].y
    # Checks if the middle fingertip (12) is above its lower joint (10)
    middle_up = lm[12].y < lm[10].y
    # Checks if the ring fingertip (16) is above its lower joint (14)
    ring_up = lm[16].y < lm[14].y
    # Checks if the pinky fingertip (20) is above its lower joint (18)
    pinky_up = lm[20].y < lm[18].y

    if label == "Right":
        # For the right hand, the thumb is "up" (extended) when its tip (4) is to the left of its lower joint (3)
        thumb_up = lm[4].x < lm[3].x
    else:
        # For the left hand, the thumb is "up" when its tip (4) is to the right of its lower joint (3)
        thumb_up = lm[4].x > lm[3].x

    # Calculates the pixel distance between the thumb tip (4) and the index fingertip (8)
    pinch_distance = distance(lm[4], lm[8], w, h)
    # Calculates the pixel distance between the wrist base (0) and the middle knuckle (9) to estimate hand size
    hand_size = distance(lm[0], lm[9], w, h)

    if hand_size > 0:
        # Normalizes the pinch distance by hand size so the ratio is consistent regardless of how close the hand is to the camera
        pinch_ratio = pinch_distance / hand_size
    else:
        pinch_ratio = 1  # Defaults to 1 (no pinch) if hand size is zero to avoid division by zero

    # Determines if a pinch gesture is active: ratio below 0.35 means thumb and index are close together
    thumb_index_pinch = pinch_ratio < 0.35

    # Gesture 8 (OK sign): thumb and index are pinched together, while middle, ring, and pinky are extended
    if thumb_index_pinch and middle_up and ring_up and pinky_up:
        return 8, "Gesture 8: OK"

    # Gesture 7 (Love You / ILY sign): thumb, index, and pinky are up; middle and ring are down
    if thumb_up and index_up and not middle_up and not ring_up and pinky_up:
        return 7, "Gesture 7: Love You"

    # Gesture 6 (Hang Loose / Shaka): thumb and pinky are up; index, middle, and ring are down
    if thumb_up and not index_up and not middle_up and not ring_up and pinky_up:
        return 6, "Gesture 6: Hang Loose"

    # Gesture 9 (Middle Finger): only the middle finger is extended; all others are down
    if not thumb_up and not index_up and middle_up and not ring_up and not pinky_up:
        return 9, "Gesture 9: Middle Finger"

    # Gesture 5 (Open Hand): all five fingers are extended
    if thumb_up and index_up and middle_up and ring_up and pinky_up:
        return 5, "Gesture 5: Five / Open Hand"

    # Gesture 4 (Four fingers): all fingers except the thumb are extended
    if not thumb_up and index_up and middle_up and ring_up and pinky_up:
        return 4, "Gesture 4: Four"

    # Gesture 3 (Three fingers): index, middle, and ring are extended; thumb and pinky are down
    if not thumb_up and index_up and middle_up and ring_up and not pinky_up:
        return 3, "Gesture 3: Three"

    # Gesture 2 (Peace / Two): index and middle fingers are extended; others are down
    if not thumb_up and index_up and middle_up and not ring_up and not pinky_up:
        return 2, "Gesture 2: Two / Peace"

    # Gesture 1 (Pointing / One): only the index finger is extended
    if not thumb_up and index_up and not middle_up and not ring_up and not pinky_up:
        return 1, "Gesture 1: One"

    # Gesture 0 (Fist): all fingers are folded down, including the thumb
    if not thumb_up and not index_up and not middle_up and not ring_up and not pinky_up:
        return 0, "Default: Fist"

    return None, "Unknown Gesture"  # Returns None if the finger combination doesn't match any defined gesture

# Main loop — runs continuously to process each webcam frame
while True:
    success, img = cam.read()  # Captures a single frame from the webcam; success is False if the frame couldn't be read
    if not success:
        break  # Exits the loop if the camera fails to return a valid frame

    img = cv2.flip(img, 1)      # Mirrors the image horizontally so it behaves like a mirror (left/right matches user's perspective)
    h, w, _ = img.shape         # Extracts the frame height and width in pixels; ignores the color channel count

    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Converts the frame from BGR (OpenCV default) to RGB (required by MediaPipe)
    results = hands.process(rgb)                # Runs MediaPipe hand detection on the RGB frame and returns landmark results

    if results.multi_hand_landmarks and results.multi_handedness:  # Checks if at least one hand was detected in the frame
        hand_landmarks = results.multi_hand_landmarks[0]           # Gets the landmark data for the first detected hand
        handedness = results.multi_handedness[0]                   # Gets the handedness classification for the first detected hand
        label = handedness.classification[0].label                 # Extracts the label string: either "Left" or "Right"

        if label == "Right":  # Only processes and sends gestures when a right hand is detected

            mp_draw.draw_landmarks(
                img,                        # The video frame to draw on
                hand_landmarks,             # The 21 landmark points to draw
                mp_hands.HAND_CONNECTIONS   # The predefined connections between landmarks (draws the skeleton lines)
            )

            # Calls the gesture recognition function and unpacks the gesture number and display text
            gesture_number, gesture_text = recognize_gesture(hand_landmarks, label, w, h)

            if gesture_number is not None and gesture_number != last_sent:  # Only sends if a valid gesture was detected and it's different from the last one sent
                value = write_read(gesture_number)  # Sends the gesture number to the Arduino and reads its response
                print(value)                        # Prints the Arduino's response to the console for debugging
                last_sent = gesture_number          # Updates last_sent so the same gesture isn't repeatedly transmitted

            cv2.putText(
                img,                            # The frame to draw text on
                "Keep Palm Facing The Camera",  # Instruction text shown to the user
                (20, 40),                       # Position of the text (x=20, y=40 pixels from top-left)
                cv2.FONT_HERSHEY_SIMPLEX,       # Font style
                0.8,                            # Font scale (size)
                (0, 0, 255),                    # Text color in BGR: red
                2                               # Line thickness in pixels
            )

            cv2.putText(
                img,            # The frame to draw text on
                gesture_text,   # The gesture name/label recognized in the current frame
                (20, 80),       # Position of the text (x=20, y=80 pixels)
                cv2.FONT_HERSHEY_SIMPLEX,  # Font style
                0.8,            # Font scale
                (0, 255, 0),    # Text color in BGR: green
                2               # Line thickness
            )

            cv2.putText(
                img,                        # The frame to draw text on
                f"Sending: {gesture_number}",  # Displays which gesture number is being sent to the Arduino
                (20, 120),                  # Position of the text (x=20, y=120 pixels)
                cv2.FONT_HERSHEY_SIMPLEX,   # Font style
                0.8,                        # Font scale
                (255, 255, 0),              # Text color in BGR: cyan/yellow
                2                           # Line thickness
            )

        else:
            cv2.putText(
                img,                    # The frame to draw text on
                "Show Right Hand Only", # Prompts the user to switch to their right hand
                (20, 40),               # Position of the text
                cv2.FONT_HERSHEY_SIMPLEX,  # Font style
                0.8,                    # Font scale
                (0, 0, 255),            # Text color in BGR: red
                2                       # Line thickness
            )
            last_sent = None  # Resets last_sent so the next valid gesture will be transmitted fresh

    else:
        cv2.putText(
            img,                  # The frame to draw text on
            "No Hand Detected",   # Shown when MediaPipe finds no hand in the frame
            (20, 40),             # Position of the text
            cv2.FONT_HERSHEY_SIMPLEX,  # Font style
            0.8,                  # Font scale
            (0, 0, 255),          # Text color in BGR: red
            2                     # Line thickness
        )
        last_sent = None  # Resets last_sent since no hand is present, allowing re-detection cleanly

    cv2.imshow("Hand Volume Control", img)  # Displays the current annotated frame in a window titled "Hand Volume Control"

    if cv2.waitKey(1) & 0xFF == ord("q"):  # Waits 1ms for a keypress; if 'q' is pressed, exits the loop
        break

# Cleanup — releases all resources after the loop ends
cam.release()              # Releases the webcam so it's no longer in use
cv2.destroyAllWindows()    # Closes all OpenCV display windows
arduino.close()            # Closes the serial connection to the Arduino
