/*
    Hand / Finger Servo Controller

    This program controls 5 servos that represent fingers:

      - Thumb
      - Index
      - Middle
      - Ring
      - Pinky

    Commands are sent over the Serial Monitor as numbers 1-9. 
    Each number triggers a different hand gesture.

    ***
    
    The way the servo motors were mounted the servo motor arm's for the thumb and middle finger can physically collide depending on

    ***

    To prevent damage:

      - The thumb is NOT allowed to move while the middle finger is in the DOWN position.

    This safety logic is handled by:

      - writeThumbSafe()
      - writeThumbAndMiddle()

    The program tracks servo positions internally so it knows
    whether a movement is safe before sending commands.
*/

#include <Servo.h>

// Stores the number entered through Serial Monitor
int x;

/*
    Create servo objects.

    NOTE:
    The comments beside the names originally had incorrect pin
    numbers. The REAL pins are assigned later in setup().
*/
Servo thumb;
Servo middle;
Servo index;
Servo ring;
Servo pinky;

/*
    Define common servo positions.

    UP   = fully extended/open
    DOWN = fully bent/closed

    Using named constants makes the code easier to read and
    easier to modify later.
*/
#define UP 180
#define DOWN 0

/*
    POSITION TRACKING VARIABLES

    These variables remember the CURRENT positions of the
    thumb and middle servos.

    Why track positions?

    The Servo library itself does NOT tell us where a servo is.
    We must remember the last commanded position ourselves.

    This is critical for the safety system.
*/
int thumbPosCurrent = UP;
int middlePosCurrent = UP;

/*
    Boolean state flags.

    true  = finger is DOWN
    false = finger is UP
*/
bool thumbIsDown = false;
bool middleIsDown = false;

/*
    SAFE THUMB MOVEMENT FUNCTION

    This function protects the mechanism by blocking thumb
    movement whenever the middle finger is DOWN.

    SAFETY RULE:
      If middle finger is DOWN,
      thumb is NOT allowed to move.

    Why?

    On many robotic hand designs, these fingers can collide,
    jam, strain gears, or overload the servos.

    PARAMETERS
    ----------
    pos = desired thumb position
*/
void writeThumbSafe(int pos) {

  /*
      SAFETY CHECK

      middleIsDown:
          Checks whether middle finger is currently DOWN.

      pos != thumbPosCurrent:
          Only block movement if the thumb is ACTUALLY trying
          to move somewhere different.

      This allows harmless repeated commands like:
          writeThumbSafe(DOWN);

      without triggering a block message every time.
  */
  if (middleIsDown && pos != thumbPosCurrent) {

    Serial.println(
      "Blocked: thumb cannot move while middle is down."
    );

    // Stop immediately and DO NOT move the servo
    return;
  }

  // Safe to move thumb
  thumb.write(pos);

  // Update tracked position
  thumbPosCurrent = pos;

  // Update state flag
  thumbIsDown = (pos == DOWN);
}

/*
    SAFE MIDDLE FINGER MOVEMENT

    Currently the middle finger itself is allowed to move freely.

    However, we STILL update all tracking variables so future
    thumb safety checks work correctly.
*/
void writeMiddleSafe(int pos) {

  // Move middle servo
  middle.write(pos);

  // Update tracked position
  middlePosCurrent = pos;

  // Update DOWN state
  middleIsDown = (pos == DOWN);
}

/*
    SYNCHRONIZED THUMB + MIDDLE MOVEMENT

    This function moves BOTH servos together.

    It exists because certain gestures require coordinated
    motion between the thumb and middle finger.

    SPECIAL SAFETY LOGIC

    The key danger scenario is:

        Middle already DOWN
        +
        Thumb tries to move

    That combination is blocked.

    However:

        Thumb DOWN + Middle DOWN simultaneously

    is ALLOWED when performed together from a safe state.

    Example:
        writeThumbAndMiddle(DOWN, DOWN);

    This works because the thumb moves BEFORE the middle
    becomes dangerous.

    WHY THIS FUNCTION EXISTS

    If we used separate calls:

        writeMiddleSafe(DOWN);
        writeThumbSafe(DOWN);

    the second call would fail because middle would already
    be DOWN.

    This combined function allows carefully controlled
    synchronized movement.
*/
void writeThumbAndMiddle(int thumbPos, int middlePos) {

  /*
      SAFETY CHECK

      If middle is ALREADY DOWN,
      thumb movement is forbidden.
  */
  if (middlePosCurrent == DOWN &&
      thumbPos != thumbPosCurrent) {

    Serial.println(
      "Blocked: thumb cannot move while middle is already down."
    );

    return;
  }

  /*
      Move both servos.

      ORDER MATTERS.

      Thumb is moved first before middle enters the dangerous
      DOWN state.
  */
  thumb.write(thumbPos);
  middle.write(middlePos);

  // Update tracked positions
  thumbPosCurrent = thumbPos;
  middlePosCurrent = middlePos;

  // Update state flags
  thumbIsDown = (thumbPos == DOWN);
  middleIsDown = (middlePos == DOWN);
}

/*
    SETUP

    Runs ONCE when the Arduino powers on or resets.
*/
void setup() {

  // Start serial communication
  Serial.begin(115200);

  // Set serial timeout for readString()
  Serial.setTimeout(1);

  /*
      Attach servos to pins.

      Actual wiring:
        thumb  -> pin 5
        index  -> pin 6
        middle -> pin 9
        ring   -> pin 10
        pinky  -> pin 11
  */
  thumb.attach(5);
  index.attach(6);
  middle.attach(9);
  ring.attach(10);
  pinky.attach(11);

  /*
      Initialize hand in safe OPEN position.
  */
  writeThumbAndMiddle(UP, UP);

  index.write(UP);
  ring.write(UP);
  pinky.write(UP);

  Serial.println("Ready. Enter a number 1-9:");
}

/*
    MAIN LOOP

    Continuously waits for serial input.
*/
void loop() {

  /*
      Check whether data has arrived through Serial.
  */
  if (Serial.available() > 0) {

    /*
        Read incoming number.

        Example:
            User types "3"

        x becomes:
            3
    */
    x = Serial.readString().toInt();

    // Print confirmation
    Serial.print("You entered: ");
    Serial.println(x);

    // Gesture Case S
    switch (x) {

      case 1: // Number 1

        Serial.println("Gesture 1");

        index.write(UP);
        ring.write(DOWN);
        pinky.write(DOWN);

        writeThumbAndMiddle(DOWN, DOWN);

        /*
            Simultaneous thumb + middle movement. This movement is allowed because the servo arms move in the the same direction at the same time.
        */

        break;

      case 2: // Peace & Number 2

        Serial.println("Gesture 2");

        index.write(UP);
        ring.write(DOWN);
        pinky.write(DOWN);

        // Raise middle first
        writeMiddleSafe(UP);

        // Then thumb can safely move
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

      case 5: // Open Hand

        Serial.println("Gesture 5");

        index.write(UP);
        ring.write(UP);
        pinky.write(UP);
        
        writeMiddleSafe(UP);
        writeThumbSafe(UP);

        break;

      case 6:

        Serial.println("Gesture 6");

        /*
            Thumb must move FIRST before middle goes DOWN.
        */
        writeThumbSafe(UP);

        pinky.write(UP);
        index.write(DOWN);
        ring.write(DOWN);

        /*
            Middle goes DOWN last to avoid collision.
        */
        writeMiddleSafe(DOWN);

        break;

      case 7:

        Serial.println("Gesture 7");

        // Safe ordering again
        writeThumbSafe(UP);

        index.write(UP);
        pinky.write(UP);
        ring.write(DOWN);

        writeMiddleSafe(DOWN);

        break;

      case 8:

        Serial.println("Gesture 8");

        /*
            Raise middle BEFORE moving thumb.
        */
        writeMiddleSafe(UP);

        writeThumbSafe(DOWN);

        // Partial bend for index finger
        index.write(80);

        ring.write(UP);
        pinky.write(UP);

        break;

      case 9:

        Serial.println("Gesture 9");

        writeMiddleSafe(UP);
        writeThumbSafe(DOWN);

        index.write(DOWN);
        ring.write(DOWN);
        pinky.write(DOWN);

        break;

      default:

        /*
            Invalid input fallback.

            Moves hand into a default position.
        */
        Serial.println("Enter a number 1-9");

        index.write(DOWN);
        ring.write(DOWN);
        pinky.write(DOWN);

        writeThumbAndMiddle(DOWN, DOWN);

        break;
    }

    /*
        Small delay to allow servos time to move.
    */
    delay(200);

    /*
        Clear any leftover serial data.

        Prevents accidental repeated commands.
    */
    while (Serial.available() > 0) {
      Serial.read();
    }
  }
}