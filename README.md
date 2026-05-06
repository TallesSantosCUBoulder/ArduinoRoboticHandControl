# PID Controlled Ping Pong Ball Levitation

## Introduction
  This experiment of the Ping Pong Levitator aims to 

## Control Systems

  <img width="485" height="499" alt="image10" src="https://github.com/user-attachments/assets/8f04db30-47b2-401d-a286-e2f66904d382" />
  
  _Figure 1: Diagrams_

  
  Control 


<img width="461" height="397" alt="image6" src="https://github.com/user-attachments/assets/0156d513-a595-4a3f-8a01-977dfa4559e2" />

_Figure 2: The _

 With the 

## PID Controller

<img width="389" height="379" alt="image7" src="https://github.com/user-attachments/assets/c59ce5ee-cf6b-4f16-8037-c22c9a54751c" />

_Figure 2: The output of a control system controller and the types of variables that can affect the output. T<sub>r</sub> is the rise time, or how fast the output reaches the desired level. The overshoot is how much over the desired level the output reaches. Peak time, or T<sub>p</sub>, is how long until the overshoot value returns down to around 1% of the desired level, and the e<sub>ss</sub> is the steady-state error, or how far off the output is from the desired level._


## Hardware
### Components
- 1 x 25k Ω Potentiometer

_Figure 3: _

Paragraph.

## Results

![image9-ezgif com-resize](https://github.com/user-attachments/assets/75edd347-f2f3-47f1-adec-f2e8bb1b7d37)


_Figure 4: A GIF of the incomplete and unoptimized PID controller. While the rise time is pretty low, the overshoot is extreme, and the settling time is too high to even work._

Figure 4 is the result of manually tuning the K<sub>P</sub>, K<sub>I</sub>, and the K<sub>D</sub> values and still encountering some errors within the system. The theory of manually tuning a PID controller is to set everything to zero, and adjust K<sub>P</sub> until it oscillates around the desired level. Half that K<sub>P</sub> values and increase K<sub>I</sub> until the offset is corrected, and increase K<sub>D</sub> until the output reaches the desired value. That value was previously achieved with the values K<sub>P</sub> = 50, K<sub>I</sub> = 3, and K<sub>D</sub> = 10, but system errors and inaccuracies caused those values to not only no longer work, but to be an example of a poorly optimized PID controller.

![image11-ezgif com-resize](https://github.com/user-attachments/assets/002b208c-c737-4310-9778-2a3293591285)

_Figure 5: A GIF of the optimized PID controller with a_

The outcome of the PID controller with the low-pass filter and the K<sub>P</sub> = 15, the K<sub>I</sub> = 5, and the K<sub>D</sub> = 7.5 made for the best controller. As seen in Figure 5, there was some overshoot in the system; the peak time was short with a low steady-state error. This allowed for the system to not only get to the desired height quickly, but to stay pretty level at that same height without too many issues.

## Conclusion

  This project demonstrates the successful application of PID control to regulate the height of a ping pong ball using a closed-loop system. An ultrasonic sensor provided position feedback, while an Arduino-based PID controller adjusted fan speed through PWM control to maintain the desired height. Manual tuning showed that increasing proportional gain improved response speed but increased oscillation, integral control reduced steady-state error, and derivative control improved stability by damping oscillations. Overall, the system achieved stable levitation, proving that PID control is effective in this real-world application.

# Code Explanation

## MATLAB Serial Reader and Plotter

This program reads data sent by the Arduino through the serial port and displays it in real time. It opens the serial port /dev/ttyUSB0 at 115200 baud, clears any old data, and continuously reads incoming characters. Characters are concatenated until a newline is detected, meaning a full line of data has arrived.

Each received line is printed in the MATLAB console and parsed to extract numerical values. When exactly four numbers are found, they are stored in a data matrix. Every 100 samples, the script updates two plots: position and reference on the left, and the PWM command on the right. The loop runs continuously until the user manually stops the script in MATLAB.

To use it, upload one of the Arduino sketches, ensure the correct serial port is selected, run the MATLAB script, and observe the live plots.

## Arduino PID Controller – Version 4

## Appendix
# Equations
1. $controller(t) = u(t) = K_p e(t) + K_i\int e(t) \mathrm{d}t + K_d\frac{\mathrm{d}e(t)}{\mathrm{d}t}$
2. $Controller(s) = U(s) = K_p + \frac{K_i}{s} + K_ds$



