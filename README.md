# Arduino Robotic Hand Control

## Introduction

This project aims to demonstrate the design and construction of a robotic hand capable of mimicking common human hand gestures in real time. The system combines computer vision, Arduino control, servo motors, and 3D printed components to create a robotic hand that responds to live hand movements captured through a webcam. Using Python with OpenCV and MediaPipe, the program detects and classifies different hand gestures, then sends corresponding commands to an Arduino through serial communication. The Arduino controls five SG90 servo motors that move each finger of the robotic hand to replicate the detected gesture. This project shows how digital signal processing can be used with a few servo motors and simple 3D printed components to create robotic motion that responds to human movement in real time.

## Inspiration & Research

First, I started with a simple Google search for inspiration. I was mainly looking for an existing project with available STL files to avoid redesigning the hand and fingers from scratch. I also wanted a design that used fishing line or cables as finger tendons and was based on Arduino, since this was discussed with Professor Santos when the project was first assigned.

I found the inspiration for this project on Google Images and chose it because the design seemed simple, used an Arduino, and controlled each finger with SG90 servo motors. I also found additional images from the same project website that showed more detailed views of the assembly process, specifically how the fingers were held together using paracord and where the motors were mounted. The construction looked relatively straightforward, so I proceeded to download the STL files.

## Materials List - Basic
- 5x SG90 Servo Motors
- Approx. 150 Grams of PLA Filament & 3D Printer
- 5V 2A Power Supply
- 1x 1000 uF Capacitor
- Fishing line
- Paracord

## Materials List - Testing 
- Breadboard
- Jumper wires

_Figure 1: Diagrams_
