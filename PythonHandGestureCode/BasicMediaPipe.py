# This program uses a webcam and MediaPipe to detect a single hand in real time.
# It processes video frames, identifies whether a right hand is shown,
# draws hand landmarks if detected, and displays on-screen instructions
# based on whether a right hand is visible or not.

import cv2
import mediapipe as mp

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

            # Draw only landmarks
            mp_draw.draw_landmarks(
                img,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

            cv2.putText(
                img,
                "Keep Palm Facing The Camera",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 0, 255),
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