# Arduino Servo Control with Python

This project demonstrates how to control a servo motor connected to an Arduino board using a Python script. The Arduino sketch reads servo position commands from the serial port and moves the servo accordingly. The Python script allows the user to input servo positions and sends these commands to the Arduino via the serial port.

## Components

- Arduino board
- Servo motor
- USB cable for connecting the Arduino to the computer
- Jumper wires

## Software Requirements

- Arduino IDE
- Python 3.x
- `pyserial` Python library

## Arduino Setup

1. **Install the Arduino IDE**:
   - Download and install the Arduino IDE from the [Arduino website](https://www.arduino.cc/en/software).

2. **Connect the Arduino**:
   - Connect your Arduino board to your computer using a USB cable.

3. **Upload the Sketch**:
   - Open the Arduino IDE.
   - Load the `sketch_jul05a.ino` file.
   - Select the correct board and port from the Tools menu.
   - Click the upload button to upload the sketch to the Arduino.

### `sketch_jul05a.ino`

```cpp
#include <Servo.h>

Servo myservo;  // create servo object to control a servo
// twelve servo objects can be created on most boards

int pos = 0;    // variable to store the servo position

void setup() {
  Serial.begin(9600);
  myservo.attach(9);  // attaches the servo on pin 9 to the servo object
}

void loop() {
  if (Serial.available() > 0) {
    int val = Serial.parseInt();
    if (val >= 0 && val <= 180) {
      myservo.write(val);              // tell servo to go to position in variable 'val'
      delay(15);                       // waits 15ms for the servo to reach the position
      Serial.print("Moved to ");
      Serial.println(val);
    } else {
      Serial.println("Value out of range");
    }
  }
}
