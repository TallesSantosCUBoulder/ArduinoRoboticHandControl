# This program communicates with an Arduino over a serial connection.
# It repeatedly asks the user to enter a number, sends that number to the Arduino,
# waits for a response, and then prints whatever data the Arduino sends back.

import serial
import time

# make sure the port is the correct one -> this is dependent on which port the Arduino IDE is using
arduino = serial.Serial(port='/dev/cu.usbmodem14301', baudrate=115200, timeout=.1)


def write_read(x):
    arduino.write(bytes(x, 'utf-8'))
    time.sleep(0.05)
    data = arduino.readline()
    return data


while True:
    num = input("Enter a number: ")
    value = write_read(num)
    print(value)