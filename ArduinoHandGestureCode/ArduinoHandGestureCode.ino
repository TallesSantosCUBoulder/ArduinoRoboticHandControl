/*
    Hand / Finger Servo Controller

    Controls 5 servos representing thumb, index, middle, ring, and pinky.
    Serial input (1–9) triggers different hand gestures.

    Safety note:
    Thumb and middle finger can physically collide, so movement is restricted.

    Safety is handled by:
      - writeThumbSafe()
      - writeThumbAndMiddle()
*/

#include <Servo.h>

// Serial input value
int x;

// Servo objects for each finger
Servo thumb;
Servo middle;
Servo index;
Servo ring;
Servo pinky;

// Servo positions
#define UP 180
#define DOWN 0

// Tracks current servo positions
int thumbPosCurrent = UP;
int middlePosCurrent = UP;

// Finger state flags
bool thumbIsDown = false;
bool middleIsDown = false;

// Prevents thumb movement when middle finger is down
void writeThumbSafe(int pos) {

  if (middleIsDown && pos != thumbPosCurrent) {
    Serial.println("Blocked: thumb cannot move while middle is down.");
    return;
  }

  thumb.write(pos);
  thumbPosCurrent = pos;
  thumbIsDown = (pos == DOWN);
}

// Updates middle finger state safely
void writeMiddleSafe(int pos) {

  middle.write(pos);
  middlePosCurrent = pos;
  middleIsDown = (pos == DOWN);
}

// Moves thumb and middle together safely
void writeThumbAndMiddle(int thumbPos, int middlePos) {

  if (middlePosCurrent == DOWN && thumbPos != thumbPosCurrent) {
    Serial.println("Blocked: thumb cannot move while middle is already down.");
    return;
  }

  thumb.write(thumbPos);
  middle.write(middlePos);

  thumbPosCurrent = thumbPos;
  middlePosCurrent = middlePos;

  thumbIsDown = (thumbPos == DOWN);
  middleIsDown = (middlePos == DOWN);
}

// Runs once at startup
void setup() {

  Serial.begin(115200);
  Serial.setTimeout(1);

  // Attach servos to pins
  thumb.attach(5);
  index.attach(6);
  middle.attach(9);
  ring.attach(10);
  pinky.attach(11);

  // Start in open position
  writeThumbAndMiddle(UP, UP);

  index.write(UP);
  ring.write(UP);
  pinky.write(UP);

  Serial.println("Ready. Enter a number 1-9:");
}

// Main loop for reading commands
void loop() {

  if (Serial.available() > 0) {

    x = Serial.readString().toInt();

    Serial.print("You entered: ");
    Serial.println(x);

    switch (x) {

      case 1: // Number one
        Serial.println("Gesture 1");

        index.write(UP);
        ring.write(DOWN);
        pinky.write(DOWN);
        writeThumbAndMiddle(DOWN, DOWN);
        break;

      case 2: // Number two / peace
        Serial.println("Gesture 2");

        index.write(UP);
        ring.write(DOWN);
        pinky.write(DOWN);

        writeMiddleSafe(UP);
        writeThumbSafe(DOWN);
        break;

      case 3: // Number 3
        Serial.println("Gesture 3");

        index.write(UP);
        ring.write(UP);
        pinky.write(DOWN);

        writeMiddleSafe(UP);
        writeThumbSafe(DOWN);
        break;

      case 4: // Number 4 
        Serial.println("Gesture 4");

        index.write(UP);
        ring.write(UP);
        pinky.write(UP);

        writeMiddleSafe(UP);
        writeThumbSafe(DOWN);
        break;

      case 5: // Number 5 / Open Hand
        Serial.println("Gesture 5");

        index.write(UP);
        ring.write(UP);
        pinky.write(UP);

        writeMiddleSafe(UP);
        writeThumbSafe(UP);
        break;

      case 6: // Hang Loose
        Serial.println("Gesture 6");

        writeThumbSafe(UP);

        pinky.write(UP);
        index.write(DOWN);
        ring.write(DOWN);

        writeMiddleSafe(DOWN);
        break;

      case 7: // I Love You (ASL)
        Serial.println("Gesture 7");

        writeThumbSafe(UP);

        index.write(UP);
        pinky.write(UP);
        ring.write(DOWN);

        writeMiddleSafe(DOWN);
        break;

      case 8: // OK 
        Serial.println("Gesture 8");

        writeMiddleSafe(UP);
        writeThumbSafe(DOWN);

        index.write(80);
        ring.write(UP);
        pinky.write(UP);
        break;

      case 9: // Pointing Up
        Serial.println("Gesture 9");

        writeMiddleSafe(UP);
        writeThumbSafe(DOWN);

        index.write(DOWN);
        ring.write(DOWN);
        pinky.write(DOWN);
        break;

      default:
        Serial.println("Enter a number 1-9");

        index.write(DOWN);
        ring.write(DOWN);
        pinky.write(DOWN);

        writeThumbAndMiddle(DOWN, DOWN);
        break;
    }

    delay(200);

    while (Serial.available() > 0) {
      Serial.read();
    }
  }
}