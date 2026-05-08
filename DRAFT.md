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
- 150 grams of PLA Filament & 3D Printer
- 1x 5V 2A USB Power Supply
- 1x Spliced USB Cable
- 1x 1000 uF Capacitor
- 5ft of Fishing Line
- 5ft of Paracord
- 5x Rubber Bands

### Additional Materials - Testing
- 1x Breadboard
- 17x Jumper wires

### Printing Process

### Robotic Hand Assembly

#### System Overview

#### Directions: Mechnaincal Component Assembly

#### Directions: Electrical Component Assembly

#### Construction Proccess & Fine Tuning Finger Movement

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
