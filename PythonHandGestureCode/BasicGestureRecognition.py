import cv2
import mediapipe as mp
import math

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

def distance(p1, p2, w, h):
    x1, y1 = int(p1.x * w), int(p1.y * h)
    x2, y2 = int(p2.x * w), int(p2.y * h)
    return math.hypot(x2 - x1, y2 - y1)

def recognize_gesture(hand_landmarks, label, w, h):
    lm = hand_landmarks.landmark

    # Finger tip and pip joints
    index_up = lm[8].y < lm[6].y
    middle_up = lm[12].y < lm[10].y
    ring_up = lm[16].y < lm[14].y
    pinky_up = lm[20].y < lm[18].y

    # Thumb check depends on handedness
    if label == "Right":
        thumb_up = lm[4].x < lm[3].x
    else:
        thumb_up = lm[4].x > lm[3].x

    # Pinch / OK sign check
    pinch_distance = distance(lm[4], lm[8], w, h)
    hand_size = distance(lm[0], lm[9], w, h)

    if hand_size > 0:
        pinch_ratio = pinch_distance / hand_size
    else:
        pinch_ratio = 1

    thumb_index_pinch = pinch_ratio < 0.35

    # Gesture 8: Thumb + index pinch
    if thumb_index_pinch and middle_up and ring_up and pinky_up:
        return "Gesture 8: OK"

    # Gesture 7: Thumb + index + pinky up
    if thumb_up and index_up and not middle_up and not ring_up and pinky_up:
        return "Gesture 7: Love You"

    # Gesture 6: Thumb + pinky up
    if thumb_up and not index_up and not middle_up and not ring_up and pinky_up:
        return "Gesture 6: Hang Loose"

    # Gesture 9: Middle finger up
    if not thumb_up and not index_up and middle_up and not ring_up and not pinky_up:
        return "Gesture 9: Middle Finger"

    # Gesture 5: All fingers up
    if thumb_up and index_up and middle_up and ring_up and pinky_up:
        return "Gesture 5: Five / Open Hand"

    # Gesture 4: Four fingers up, no thumb
    if not thumb_up and index_up and middle_up and ring_up and pinky_up:
        return "Gesture 4: Four"

    # Gesture 3: Index + middle + ring up
    if not thumb_up and index_up and middle_up and ring_up and not pinky_up:
        return "Gesture 3: Three"

    # Gesture 2: Index + middle up
    if not thumb_up and index_up and middle_up and not ring_up and not pinky_up:
        return "Gesture 2: Two / Peace"

    # Gesture 1: Index finger up
    if not thumb_up and index_up and not middle_up and not ring_up and not pinky_up:
        return "Gesture 1: One"

    # Default: fist
    if not thumb_up and not index_up and not middle_up and not ring_up and not pinky_up:
        return "Default: Fist"

    return "Unknown Gesture"

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

            gesture = recognize_gesture(hand_landmarks, label, w, h)

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
                gesture,
                (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
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

    cv2.imshow("Hand Volume Control", img)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Cleanup
cam.release()
cv2.destroyAllWindows()