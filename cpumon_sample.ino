#include <Servo.h>

//Make a Servo object
Servo myservo;

void setup() {
  //Start serial communication
  Serial.begin(115200);
  //Attach pin 11 to the Servo object
  myservo.attach(11);
  //Prepare on launch, by resetting to zero
  myservo.write(0);
}

//Make these variables for later
int newNum;
int prevNum;

void loop() {
  //Check if there's anything to read from Serial
  if (Serial.available()) {
    //Set previous number
    prevNum = newNum;
    //Get the new integer sent via Serial
    newNum = Serial.parseInt();
  }
  //Check if the new number differs from the previous one, otherwise changes are unnecessary
  //Also does nothing if the previous block didn't run due to there being no new input
  if (newNum != prevNum) {
    //Write the current input to the servo
    myservo.write(newNum);
    //Give it a moment just in case (garbled input, etc)
    delay(100);
  }
}
