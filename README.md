# Arduino Robotic Hand Control

## Introduction

This project aims to demonstrate the design and construction of a robotic hand capable of mimicking common human hand gestures in real time. The system combines computer vision, Arduino control, servo motors, and 3D printed components to create a robotic hand that responds to hand movements captured  by webcam. 

Using OpenCV and MediaPipe, the Python program detects and classifies different hand gestures, then sends the corresponding commands to an Arduino through serial communication. The Arduino controls five SG90 servo motors that move each finger of the robotic hand to replicate the detected gesture. 

This project demonstrates how a few servo motors and simple 3D printed components can be used to create interactive robotic motion.

_Figure: GIF of Open & Close Hand Movement_ 

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

I modified the STL files from the Thingiverse link above. The arm piece needed to be scaled down to 10% of its original size. After this, I imported the files into my printer’s slicer software.

For the print settings, I specified auto tree supports, no brim, and 15% infill for the arm, fingers, and arm stand. For the hand, I used the same settings but without supports so that there would be no plastic obstructing the holes where the fishing line will eventually pass through. I oriented the hand and arm in a vertical position, while the fingers were laid flat. Each file was printed separately in case of a misprint.

### Robotic Hand Assembly

#### System Overview

The robotic hand is made up of 3D printed parts, strings, rubber bands, and servo motors. The printed parts form the shape of the hand and fingers and keep everything in place. Paracord runs through the fingers to guide how they bend and help them move smoothly. Fishing line connects each finger to a servo motor and acts like a tendon that pulls the fingers closed when the motor turns. Rubber bands help pull the fingers back open after they are bent. The servo motors control the movement by pulling or releasing the fishing line based on electrical signals, allowing each finger to move and form different gestures.

#### Mechanical Component Assembly Instructions

- Remove all supports from the 3D printed parts.
- Cut the paracord and melt one end to make it easier to thread through the holes.
- Starting with the pinky finger, feed the melted end of the paracord up through each segment on the left side of the finger, then back down through the right side, leaving about 6 inches of excess cord on both ends.
- Repeat this process for the ring finger, then continue until all five fingers are threaded.
- Cut the paracord between each finger so each finger has its own separate line.
- Next, cut five pieces of fishing line, each about one foot long. Tie a double fisherman’s knot on one end of each line.
- Feed the untied end of the fishing line through the hole at the tip of each finger. The knot should prevent it from pulling through completely.
- Then, route both the paracord and fishing lines through the corresponding holes in the hand piece.
- Tie the paracord for each finger using an overhand knot, leaving about 1 cm of slack between finger segments so they can bend properly.
- Feed the fishing lines from the hand piece into the corresponding holes in the arm piece.
- Secure the bottom of the hand to the top of the arm piece using hot glue.
- Mount five servo motors onto the arm piece using hot glue, positioning them as shown in Figure X.
- Attach single-sided servo arms to each motor using screws.
- Tie each fishing line to its corresponding servo arm using a double fisherman’s knot (see Figure X).
- Align all servo arms so that when they point toward the top of the hand, the fingers are extended, and when they rotate away from the fingers, the fingers curl into a fist.
- Finally, attach a rubber band to the tip of each finger using a girth hitch. Tie an overhand knot at the base of each finger, leaving a loop large enough to wrap around the paracord knot at the knuckle.

_Figure: Image of knots on the back of the hand_
_Figure: Image of knots on the fingertips_
_Figure: Image of servo motor configuration & knots - fully opened & closed (side by side)_
_Figure: Image of wiring coming out of arm_ 

#### Directions: Electrical Component Assembly
- Identify all five servo motors and label them (e.g., Thumb, Index, Middle, Ring, Pinky) to avoid wiring confusion.
- Connect each servo motor to the Arduino:
  - Connect signal wires to separate PWM-capable digital pins.
  - Connect all power (VCC) wires together to a 5V 2A external power supply.
  - Connect all ground (GND) wires together and ensure a common ground between the external power supply and the microcontroller.
  - Place a 1000 µF electrolytic capacitor across the 5V and GND rails near the servos to help smooth current spikes.
- Ensure the ground of the external power supply is connected to the Arduino's ground.
- Organize the cables and glue them to the base of the arm stand piece as shown in Figure X.
- Upload or connect control code (such as Arduino servo control code) to test each servo individually.
- Calibrate servo positions so that:
  - One direction corresponds to “finger extended”
  - The opposite direction corresponds to “finger curled”

_Figure : Circuit Schematic_
_Figure : Image of breadboard_

## Software

### System Overview

_Figure : Simple System Diagram (Camera -> MediaPipe -> Case Recognition -> Serial Port Communication -> Hand Gesture Replication)_ <br><br>

### System Setup & Execution

Visual Studio Code is used as the development environment to write and run Python code, while Miniconda is used to manage the Python setup and environments. A dedicated virtual environment was created specifically for this project, including its own Python version and libraries, which keeps the project separate from other Python projects. The project uses several libraries, including OpenCV for video capture and image processing, MediaPipe for hand tracking, math for distance calculations, subprocess for running external system commands for volume control, threading for running tasks in parallel, and time for time-related functions such as delays and timestamps.

### MediaPipe & Open CV - Explained

OpenCV captures video from the webcam, preprocesses each frame, draws visual elements on the screen, marks the thumb and index finger positions, draws a line between the fingers, displays volume and coordinate data, and outputs the video stream. OpenCV handles camera input, image processing, and display, while MediaPipe strictly handles hand tracking and landmark detection.

MediaPipe Hands is a high-fidelity hand and finger tracking solution that employs machine learning to infer 21 three-dimensional landmarks of a hand from a single frame [1]. The system relies on these landmarks, shown in Figure 1, to determine finger positions and compute distances for gesture-based control. The names of these landmarks are shown in Figure 2. The MediaPipe library manages several parameters, including static image mode, maximum number of hands, model complexity, minimum detection confidence, minimum tracking confidence, multi-handedness, and multi-hand landmarks.

_Figure : Hand landmark model showing 21 key-points corresponding to 21 hand-knuckle coordinates [1]._

_Figure : Hand landmark names indexed from 0 to 20 [1]._

The thumb and index finger positions are obtained as pixel coordinates, as shown in Figure 3. The distance between the two fingers is then calculated using the Euclidean distance formula shown in Eq. 1. In the code, this is implemented using a function that computes the straight-line distance in pixels between the thumb and index finger, as shown in Figure 4.

_Figure : Image of thumb and index finger coordinates._

```math
d = \sqrt{(x_2 - x_1)^2 + (y_2 - y_1)^2}
```
<p align="right"><em>Equation 1: Distance Equation</em></p>

The xxx code focuses on performing a basic distance calculation between the thumb and index fingers, as shown in Figures 5 and 6. However, I quickly realized that the distance between these fingers would need to be normalized. From the camera’s point of view, the distance between the fingers increases and decreases depending on how close the hand is to the camera, which would cause the volume to change based on the hand’s position in the frame. A message also needed to be displayed to instruct the user to keep the palm of the hand normal to the camera, since the distance between the fingers is calculated using two-dimensional coordinates. Rotating the fingers so that they overlap can cause the distance to shrink to zero from the camera’s perspective. After making these changes, I moved on to the next iteration, which focuses on mapping the distance to the system volume control.

### Arduino Code Explanation

#### Servo Arm Collision Safety Logic
- The collision safety logic is implemented in two functions: writeThumbSafe() and writeThumbAndMiddle().
  - In writeThumbSafe(), thumb movement is blocked whenever middleIsDown == true, preventing any independent thumb motion that could interfere with the middle finger’s position.
  - In writeThumbAndMiddle(), the system performs a similar check using middlePosCurrent == DOWN. If the middle finger is already down, any combined update that would also move the thumb is prevented to avoid unsafe transitions.
- Both functions rely on stored state variables (middleIsDown, middlePosCurrent) to make sure that the thumb is only allowed to move when the middle finger is not in a potentially conflicting position.

### Python Code Explanation

## Results

_Figure: GIF of all 9 gestures_

## Conclusion

## Future Improvements

## Acknowledgements

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
  
## Images
<img width="30%" alt="unnamed-1" src="https://github.com/user-attachments/assets/3b29622f-c6d6-4541-a29a-b013c0f2ee0e" />

## Information
* In what order should the to programs be run -> you should close the serial port on the arduino after you run it so the python script can access it -> why do you need to do this -> simple explanation
* what do you need to change in the code depending -> com port name
* What libraries do you need installed on to work the python code -> media pipe, open cv, ect
* how was the virtual environment set up and why -> grab explanation from previous report
* what libraries does the arduino code need to work properly ->



