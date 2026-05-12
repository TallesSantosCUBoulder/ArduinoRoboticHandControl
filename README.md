# Arduino Robotic Hand Control

## Introduction

This project aims to demonstrate the design and construction of a robotic hand capable of mimicking common human hand gestures in real time. The system combines computer vision, Arduino control, servo motors, and 3D printed components to create a robotic hand that responds to hand movements captured by webcam. 

Using OpenCV and MediaPipe, the Python program detects and classifies different hand gestures, then sends the corresponding commands to an Arduino through serial communication. The Arduino controls five SG90 servo motors that move each finger of the robotic hand to replicate the detected gesture. 

This project demonstrates how a few servo motors and simple 3D printed components can be used to create interactive robotic motion.

_Figure 1: GIF of Open & Close Hand Movement_ 

## Inspiration & Research

First, I started with a simple Google search for inspiration. I was mainly looking for an existing project with available STL files to avoid redesigning the hand and fingers from scratch. I also wanted a design that used fishing line or cables as finger tendons and was Arduino friendly, since this was discussed with Professor Santos when the project was first assigned.

I found the inspiration for this project on Google Images and chose it because the design seemed simple, used an Arduino, and controlled each finger with SG90 servo motors. I also found additional images from the same project website that showed more detailed views of the assembly process, specifically how the fingers were held together using paracord and where the motors were mounted. The construction looked relatively straightforward, so I proceeded to download the STL files.

Link to Inspiration: https://www.thingiverse.com/thing:4807141/files

## Methodology

### 3D Printing & Finger Movement

- The hand components were printed in PLA filament. Each finger was printed in multiple segments connected with paracord joints to allow realistic bending motion. Fishing line was threaded through channels inside each finger and connected to a servo motor mounted in the forearm so when each servo arm rotates the corresponding finger bends inward.

### Circuit Design

- Each SG90 servo motor was connected to the Arduino using PWM pins. Since multiple servos can draw significant current simultaneously, an external 5V power supply was used instead of powering the servos directly from the Arduino. A 1000 µF capacitor was added across the power rails to reduce voltage drops and servo jitter.

### Gesture Detection

- Python was used with OpenCV and MediaPipe to process webcam video in real time. MediaPipe identifies 21 hand landmarks that represent joints and fingertip locations. The software compares landmark positions to determine whether fingers are extended or bent.

### Serial Communication

- When a gesture is detected, Python sends a simple command string over serial communication to the Arduino. The Arduino interprets the command and adjusts the servo's arm positions to imitate the detected finger positions.

## Hardware

### Basic Materials List
- 1x Arduino Uno
- 5x SG90 Servo Motors
- 200 grams of PLA Filament & 3D Printer
- 1x 5V 2A USB Power Supply
- 1x Spliced USB Cable
- 1x 1000 uF Capacitor
- 5ft of Fishing Line
- 10ft of Paracord
- 5x Rubber Bands

### Additional Materials - Testing
- 1x Breadboard
- 17x Jumper wires

### Printing Process

I modified the STL files from the Thingiverse link above. The arm piece needed to be scaled down to 10% of its original size. After this, I imported the files into my printer's slicer software. For the print settings, I specified auto tree supports, no brim, and 15% infill for the arm, fingers, and arm stand. For the hand, I used the same settings but without supports so that there would be no plastic obstructing the holes where the fishing line will eventually pass through. I oriented the hand and arm in a vertical position, while the fingers were laid flat. Each file was printed separately in case of a misprint.

### Robotic Hand Assembly

#### System Overview

The robotic hand is made up of 3D printed parts, fishing line, rubber bands, and servo motors. The printed parts form the shape of the hand and fingers and keep everything in place. Paracord runs through the fingers to guide how they bend and help them move smoothly. Fishing line connects each finger to a servo motor and acts like a tendon that pulls the fingers closed when the motor turns. Rubber bands help pull the fingers back open after they are bent. The servo motors control the movement by pulling or releasing the fishing line based on electrical signals, allowing each finger to move and form different gestures.

#### Mechanical Component Assembly Instructions

- Remove all supports from the 3D printed parts.
- Cut the paracord and melt one end to make it easier to thread through the holes.
- Starting with the pinky finger, feed the melted end of the paracord up through each segment on the left side of the finger, then back down through the right side, leaving about 6 inches of excess cord on both ends.
- Repeat this process for the ring finger, then continue until all five fingers are threaded.
- Cut the paracord between each finger so each finger has its own separate line.
- Next, cut five pieces of fishing line, each about one foot long. Tie a double fisherman's knot on one end of each line.
- Feed the untied end of the fishing line through the hole at the tip of each finger. The knot should prevent it from pulling through completely.
- Then, route both the paracord and fishing lines through the corresponding holes in the hand piece.
- Tie the paracord for each finger using an overhand knot, leaving about 1 cm of slack between finger segments so they can bend properly.
- Feed the fishing lines from the hand piece into the corresponding holes in the arm piece.
- Secure the bottom of the hand to the top of the arm piece using hot glue.
- Mount five servo motors onto the arm piece using hot glue, positioning them as shown in Figure 2.
- Attach single-sided servo arms to each motor using screws.
- Tie each fishing line to its corresponding servo arm using a double fisherman's knot (see Figure 2).
- Align all servo arms so that when they point toward the top of the hand, the fingers are extended, and when they rotate away from the fingers, the fingers curl into a fist.
- Finally, attach a rubber band to the tip of each finger using a girth hitch. Tie an overhand knot at the base of each finger, leaving a loop large enough to wrap around the paracord knot at the knuckle.

_Figure 2: Image of servo motor configuration & knots - fully opened & closed (side by side)_

_Figure 3: Image of knots on the back of the hand_

_Figure 4: Image of knots on the fingertips_

_Figure 5: Image of wiring coming out of arm_ 

#### Directions: Electrical Component Assembly

- Identify all five servo motors and label them (e.g., Thumb, Index, Middle, Ring, Pinky) to avoid wiring confusion.
- Connect each servo motor to the Arduino:
  - Connect signal wires to separate PWM-capable digital pins.
  - Connect all power (VCC) wires together to a 5V 2A external power supply.
  - Connect all ground (GND) wires together and ensure a common ground between the external power supply and the microcontroller.
  - Place a 1000 µF electrolytic capacitor across the 5V and GND rails near the servos to help smooth current spikes.
- Ensure the ground of the external power supply is connected to the Arduino's ground.
- Organize the cables and glue them to the base of the arm stand piece as shown in Figure 5.
- Upload or connect control code (such as Arduino servo control code) to test each servo individually.
- Calibrate servo positions so that:
  - One direction corresponds to "finger extended"
  - The opposite direction corresponds to "finger curled"

_Figure 6: Circuit Schematic_

_Figure 7: Image of breadboard_

## Software

### System Overview

The software system consists of two programs that work together to detect hand gestures and replicate them on the robotic hand. The Python script runs on a computer and uses the webcam to capture video in real time. Each frame is processed by MediaPipe, which detects 21 hand landmarks and passes them to a gesture recognition function. That function evaluates which fingers are extended or curled and maps the result to one of nine predefined gestures, numbered 1 through 9. Once a new gesture is identified, Python sends the corresponding number to the Arduino over a USB serial connection. The Arduino receives the number, matches it to a switch case, and drives the five servo motors to the positions that replicate that gesture on the robotic hand.

Before running the Python script, the Arduino code must be uploaded and the Arduino IDE serial monitor must be closed. If the serial monitor remains open, the Python script cannot access the COM port and will throw a connection error. After uploading, the Python script is launched from within the Conda virtual environment. The only value that may need to be changed between machines is the serial port name at the top of the Python file. On macOS it appears as `/dev/cu.usbmodemXXXX`, and on Windows it appears as `COMX`, where X is the port number assigned by the operating system. This value can be found in the Arduino IDE under Tools → Port.

The overall software and hardware communication process is shown in Figures 8 and 9.

<img width="500" alt="System Flowchart 1"
src="https://github.com/user-attachments/assets/f12f0fca-d8da-4688-acba-a19808f56032" />

_Figure 8: System Flowchart (1 of 2)_

<img width="500" alt="System Flowchart 2"
src="https://github.com/user-attachments/assets/1a9477ac-9001-4020-8743-262b881d3931" />

_Figure 9: System Flowchart (2 of 2)_

### Arduino Code Explanation

#### Serial Communication & Command Handling

The Arduino is configured to communicate at a baud rate of 115200, which must match the baud rate set in the Python script. In the main `loop()`, the Arduino checks whether data is available on the serial port. When a value arrives, it is read as a string and converted to an integer using `toInt()`. That integer is passed into a `switch` statement that maps each value from 1 to 9 to a specific gesture. Any value outside this range falls into the `default` case, which closes all fingers into a fist position. A 200-millisecond delay is added after each command is processed, and any remaining bytes in the serial buffer are flushed to prevent leftover input from triggering unintended gesture changes.

#### Arduino Library Requirements

The Arduino code uses the built-in `Servo.h` library, which comes pre-installed with the Arduino IDE and does not need to be downloaded separately. No additional libraries are required. It is included at the top of the sketch with:

```cpp
#include <Servo.h>
```

#### Servo Pin Assignments & Initialization

The five servos are attached to PWM-capable digital pins during `setup()`. The pin assignments are as follows:

| Finger | Pin |
| ------ | --- |
| Thumb  | 5   |
| Index  | 6   |
| Middle | 9   |
| Ring   | 10  |
| Pinky  | 11  |

On startup, all servos are moved to the UP (180°) position so the hand begins in a fully open state. The `writeThumbAndMiddle()` function is used for the initial positioning of the thumb and middle finger to ensure the safety logic runs correctly from the start.

#### Servo Position Mapping

Each servo uses two defined positions: `UP` is set to 180 degrees and corresponds to a finger in the extended position, and `DOWN` is set to 0 degrees and corresponds to a finger that is fully curled. These values may need to be adjusted slightly depending on how the fishing line was tensioned and how the servo arms were attached during assembly. The index servo in Gesture 8 is set to 80 degrees rather than a full UP or DOWN position, which places it at a partially bent angle to form a convincing OK shape alongside the pinched thumb.

#### Servo Arm Collision Safety Logic

* The collision safety logic is implemented in two functions: writeThumbSafe() and writeThumbAndMiddle().

  * In writeThumbSafe(), thumb movement is blocked whenever middleIsDown == true, preventing any independent thumb motion that could interfere with the middle finger's position.
  * In writeThumbAndMiddle(), the system performs a similar check using middlePosCurrent == DOWN. If the middle finger is already down, any combined update that would also move the thumb is prevented to avoid unsafe transitions.
* Both functions rely on stored state variables (middleIsDown, middlePosCurrent) to make sure that the thumb is only allowed to move when the middle finger is not in a potentially conflicting position.

`writeThumbSafe()` checks the `middleIsDown` flag before allowing the thumb to move. If the middle finger is currently in the DOWN position, any command to move the thumb to a new position is blocked and a message is printed to the serial monitor. This prevents independent thumb movement while the middle finger is in a position that could cause a collision.

`writeMiddleSafe()` moves the middle servo without restriction but updates the `middleIsDown` flag and the `middlePosCurrent` variable so that subsequent thumb commands can check the current state accurately.

`writeThumbAndMiddle()` handles cases where both servos need to move at the same time. Before executing the move, it checks whether the middle finger is already in the DOWN position and whether the thumb position would actually change. If both conditions are true, the command is blocked. If the middle finger is not down, both servos are moved together and all state variables are updated in a single operation. Moving them together rather than sequentially reduces the window during which one servo could be in an unsafe intermediate position while the other has not yet moved.

### Python Code Explanation

#### Libraries & Environment Setup

Visual Studio Code is used as the development environment to write and run Python code, while Miniconda is used to manage the Python setup and environments. The project uses several libraries, including OpenCV for video capture and image processing, MediaPipe for hand tracking and math for distance calculations.

The Python script depends on the following libraries, all of which must be installed inside the virtual environment before running the script:

| Library | Install Command |
|---|---|
| `opencv-python` | `pip install opencv-python` |
| `mediapipe` | `pip install mediapipe` |
| `pyserial` | `pip install pyserial` |

A dedicated Conda virtual environment was created for this project to isolate its dependencies from other Python projects on the same machine. This prevents version conflicts between libraries and makes the project easier to reproduce. The environment was created using Miniconda with a specific Python version, and all required libraries were installed into it using `pip`. To create and activate the environment, the following commands were run in the terminal:

```bash
conda create -n robothand python=3.9
conda activate robothand
````

All required libraries were then installed into the active environment using `pip`. The environment must be activated each time before running the Python script.

#### MediaPipe & Open CV - Explained

OpenCV handles camera input, image processing, and display, while MediaPipe strictly handles hand tracking and landmark detection.

MediaPipe Hands is a high-fidelity hand and finger tracking solution that employs machine learning to infer 21 three-dimensional landmarks of a hand from a single frame [1]. The system relies on these landmarks, shown in Figure 10, to determine finger positions and compute distances for gesture-based control. The names of these landmarks are shown in Figure 11. The MediaPipe library manages several parameters, including static image mode, maximum number of hands, model complexity, minimum detection confidence, minimum tracking confidence, multi-handedness, and multi-hand landmarks.

_Figure 10: Hand landmark model showing 21 key-points corresponding to 21 hand-knuckle coordinates [1]._

_Figure 11: Hand landmark names indexed from 0 to 20 [1]._

For example, as shown in Figure 12, the thumb and index finger positions are obtained as pixel coordinates. The distance between the two fingers is then calculated using the Euclidean distance formula shown in Equation 1. In the code, this is implemented using a function that computes the straight-line distance in pixels between the thumb and index finger, as shown in Figure 12.

_Figure 12: Image of thumb and index finger coordinates._

```math
d = \sqrt{(x_2 - x_1)^2 + (y_2 - y_1)^2}
```

<p align="right"><em>Equation 1: Distance Equation</em></p>

#### Gesture Recognition Logic

The `recognize_gesture()` function receives the 21 MediaPipe landmarks for the detected hand, the handedness label (Left or Right), and the frame dimensions. It evaluates each finger independently before combining the results to identify a gesture.

For the index, middle, ring, and pinky fingers, the function compares the y-coordinate of the fingertip landmark against the y-coordinate of the proximal joint landmark below it. Because image coordinates increase downward, a fingertip with a smaller y-value than its lower joint is above it in the frame, meaning the finger is extended upward. If the fingertip y-value is greater, the finger is curled.

The thumb is handled differently because it moves laterally rather than vertically. Its state is determined by comparing the x-coordinate of the thumb tip against the x-coordinate of the joint below it. The comparison is also flipped depending on whether the hand is labeled Left or Right, since the thumb points in opposite horizontal directions for each hand.

A pinch detection check is also included to handle the OK gesture. The Euclidean distance between the thumb tip and index tip is computed using the `distance()` helper function, then divided by the distance between the wrist and the base of the middle finger to produce a normalized pinch ratio. This normalization corrects for the hand moving closer to or farther from the camera. If the ratio falls below 0.35, a pinch is registered. The order of the gesture checks in the function matters: the pinch check runs first so that the OK gesture is not misclassified as a different finger combination.

A message is also displayed to instruct the user to keep the palm of the hand normal to the camera, since the distance between the fingers is calculated using two-dimensional coordinates. Rotating the fingers so that they overlap can cause the distance to shrink to zero from the camera's perspective.

Once the finger states are evaluated, they are compared against the fixed patterns below to determine which gesture number to send to the Arduino:

| Number Sent | Gesture       | Thumb | Index | Middle | Ring | Pinky |
| ----------- | ------------- | ----- | ----- | ------ | ---- | ----- |
| 1           | One           | Down  | Up    | Down   | Down | Down  |
| 2           | Peace         | Down  | Up    | Up     | Down | Down  |
| 3           | Three         | Down  | Up    | Up     | Up   | Down  |
| 4           | Four          | Down  | Up    | Up     | Up   | Up    |
| 5           | Open Hand     | Up    | Up    | Up     | Up   | Up    |
| 6           | Hang Loose    | Up    | Down  | Down   | Down | Up    |
| 7           | I Love You    | Up    | Up    | Down   | Down | Up    |
| 8           | OK            | Pinch | —     | Up     | Up   | Up    |
| 9           | Middle Finger | Down  | Down  | Up     | Down | Down  |

The `last_sent` variable is used to prevent the same gesture number from being transmitted repeatedly on consecutive frames. A new serial command is only sent when the recognized gesture differs from the previously sent value, which reduces unnecessary traffic over the serial connection and prevents the Arduino from processing redundant inputs.

Warning: When running the two scripts, the Arduino script must be uploaded and running first. Once uploaded, close the Serial Monitor in the Arduino IDE to release the serial port. If the Serial Monitor is left open, the Python script will be unable to connect and will throw a connection error. After closing it, run the Python script to begin gesture detection.

## Results

_Figure 13: GIF of all 9 gestures_

## Conclusion

This project successfully demonstrated that a 3D printed robotic hand can replicate common human hand gestures in real time using a small number of affordable components. By combining MediaPipe's hand landmark detection with Arduino-controlled servo motors and serial communication, the system was able to recognize nine distinct gestures and translate them into physical finger movements with reasonable accuracy and low latency. The mechanical assembly, while straightforward in concept, required careful calibration of servo arm positions and fishing line tension to achieve clean and consistent finger motion. Overall, the project met its core objective of building an interactive robotic hand and served as a practical introduction to the integration of computer vision, embedded systems, and mechanical design.

## References

<table>
<tr>
<td valign="top">[1]</td>
<td>
Google, <i>MediaPipe Hands</i>, MediaPipe Documentation, 2023.<br>
Available: https://developers.google.com/mediapipe/solutions/vision/hand_landmarker
</td>
</tr>
</table>
