# Arduino Robotic Hand Control

## Introduction

This project aims to demonstrate the design and construction of a robotic hand capable of mimicking common human hand gestures in real time. The system combines computer vision, Arduino control, servo motors, and 3D printed components to create a robotic hand that responds to live hand movements captured through a webcam. 

Using Python with OpenCV and MediaPipe, the program detects and classifies different hand gestures, then sends corresponding commands to an Arduino through serial communication. The Arduino controls five SG90 servo motors that move each finger of the robotic hand to replicate the detected gesture. 

This project shows how digital signal processing can be used with a few servo motors and simple 3D printed components to create robotic motion that responds to human movement in real time.

## Inspiration & Research

First, I started with a simple Google search for inspiration. I was mainly looking for an existing project with available STL files to avoid redesigning the hand and fingers from scratch. I also wanted a design that used fishing line or cables as finger tendons and was based on Arduino, since this was discussed with Professor Santos when the project was first assigned.

I found the inspiration for this project on Google Images and chose it because the design seemed simple, used an Arduino, and controlled each finger with SG90 servo motors. I also found additional images from the same project website that showed more detailed views of the assembly process, specifically how the fingers were held together using paracord and where the motors were mounted. The construction looked relatively straightforward, so I proceeded to download the STL files.

Link to Inspiration: https://www.thingiverse.com/thing:4807141/files

## Methodology

### 3D Printing & Finger Movement
- The robotic hand components were designed and printed using PLA filament. Each finger was printed in multiple segments connected with flexible joints to allow realistic bending motion. Fishing line was threaded through channels inside each finger and connected to a servo motor mounted in forearm so when the servo arm rotate the finger bends inward.

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

For the print settings, I specified auto tree supports, no brim, and 15% infill for the arm, fingers, and arm stand. For the hand, I used the same settings but without supports so that there would be no plastic obstructing the holes where the fishing line will eventually pass through. I oriented the hand and arm in a vertical position, while the fingers were laid flat. 

Each file was printed separately in case of a misprint.

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

#### Directions: Electrical Component Assembly
- Identify all five servo motors and label them (e.g., Thumb, Index, Middle, Ring, Pinky) to avoid wiring confusion.
- Connect each servo motor to the Arduino:
  - Connect signal wires to separate PWM-capable digital pins.
  - Connect all power (VCC) wires together to a 5V 2A external power supply.
  - Connect all ground (GND) wires together and ensure a common ground between the external power supply and the microcontroller.
  - Place a 1000 µF electrolytic capacitor across the 5V and GND rails near the servos to help smooth current spikes.
    - See Figure X for detailed schematic
- Ensure the ground of the external power supply is connected to the Arduino's ground.
- Organize the cables and glue them to the base of the arm stand piece as shown in Figure X.
- Upload or connect control code (such as Arduino servo control code) to test each servo individually.
- Calibrate servo positions so that:
  - One direction corresponds to “finger extended”
  - The opposite direction corresponds to “finger curled”

## Software

### System Overview

### System Setup & Execution

### Arduino Code Explaination
- The collision safety logic is implemented in two functions: writeThumbSafe() and writeThumbAndMiddle().
  - In writeThumbSafe(), thumb movement is blocked whenever middleIsDown == true, preventing any independent thumb motion that could interfere with the middle finger’s position.
  - In writeThumbAndMiddle(), the system performs a similar check using middlePosCurrent == DOWN. If the middle finger is already down, any combined update that would also move the thumb is prevented to avoid unsafe transitions.
- Both functions rely on stored state variables (middleIsDown, middlePosCurrent) to make sure that the thumb is only allowed to move when the middle finger is not in a potentially conflicting position.

### Python Code Explaination
- MediaPipe and OpenCV explainaition from previous report
- How does the gesture recognition work exactly -> have a

## Results
- Gif of gestures 

## Conclusion

## Future Improvements

## Acknowledgements

<br><br>

# THINGS 2 ADD ->

## Figures
_Figure x: Breadboard Configuration_ <br><br>
_Figure x: Milled PCB Configuration_ <br><br>
_Figure x: Schematic of Circuit_ <br><br>
_Figure x: Simple System Diagram (Camera -> MediaPipe -> Case Recogntion -> Serial Port Communication -> Hand Gesture Replication)_ <br><br>
  
## Images
<img width="30%" alt="unnamed-1" src="https://github.com/user-attachments/assets/3b29622f-c6d6-4541-a29a-b013c0f2ee0e" />

## Information
* In what order should the to programs be run -> you should close the serial port on the arduino after you run it so the python script can access it -> why do you need to do this -> simple explaination
* what do you need to change in the code depeding -> com port name
* Whatlibraries do you ened installed on to work the python code -> media pipe, open cv, ect
* how was the virtual environment set up and why -> grab explainition from previous report
* what libraries does the arduino code need to work properly ->
