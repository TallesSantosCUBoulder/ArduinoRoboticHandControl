# Arduino Robotic Hand Control

## Introduction

This project will focus on designing and building a robotic hand that can mimic human hand gestures using computer vision and servo motors. The system will use a camera to detect hand gestures in real time and will translate those gestures into movements of a 3D-printed robotic hand. The project will integrate both hardware and software components. On the software side, Python with OpenCV and MediaPipe will be used to recognize hand gestures. On the hardware side, an Arduino will control multiple servo motors that move each finger of the robotic hand. Communication between the Python program and Arduino will be achieved through serial communication. The goal of this project will be to demonstrate real-time gesture recognition and robotic hand replication, showing how human-computer interaction can control mechanical systems.

## Control Systems

  <img width="485" height="499" alt="image10" src="https://github.com/user-attachments/assets/8f04db30-47b2-401d-a286-e2f66904d382" />
  
  _Figure 1: Diagrams_


## Hardware
### Components
- 1 x 25k Ω Potentiometer

_Figure 3: _

Paragraph.

Figure 4 is the result of manually tuning the K<sub>P</sub>, K<sub>I</sub>, and the 
