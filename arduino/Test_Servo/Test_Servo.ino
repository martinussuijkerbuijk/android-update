/* Sweep
 by BARRAGAN <http://barraganstudio.com>
 This example code is in the public domain.

 modified 8 Nov 2013
 by Scott Fitzgerald
 https://www.arduino.cc/en/Tutorial/LibraryExamples/Sweep
*/

#include <Servo.h>

Servo servoX;  // create servo object to control a servo
Servo servoY;  // create servo object to control a servo
String readString;

int pos = 0;    // variable to store the servo position

void setup() {
  servoX.attach(3);  // attaches the servo on pin 9 to the servo object
  servoY.attach(4);  // attaches the servo on pin 9 to the servo object

}

void loop() {
  while ( Serial.available() > 0) {
  int value = Serial.parseInt();

  if (Serial.read() == '\n') {
    Serial.println(value);
    servoX.write(value);
    servoY.write(value);
    }
  }
}

  
