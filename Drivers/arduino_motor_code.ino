// Include the AccelStepper Library
#include <AccelStepper.h>

//Defining the amount of steppers
const int stepperAmount = 6;

// Define pin connections
const int dirPin0 = 2;
const int stepPin0 = 3;
const int dirPin1 = 4;
const int stepPin1 = 5;
const int dirPin2 = 6;
const int stepPin2 = 7;
const int dirPin3 = 8;
const int stepPin3 = 9;
const int dirPin4 = 10;
const int stepPin4 = 11;
const int dirPin5 = 12;
const int stepPin5 = 13;

String inputString = "";
boolean stringComplete = false;
int stepNum = 1;


// Define motor interface type
#define motorInterfaceType 1


// Creates an instance

AccelStepper stepper0(motorInterfaceType, stepPin0, dirPin0);
AccelStepper stepper1(motorInterfaceType, stepPin1, dirPin1);
AccelStepper stepper2(motorInterfaceType, stepPin2, dirPin2);
AccelStepper stepper3(motorInterfaceType, stepPin3, dirPin3);
AccelStepper stepper4(motorInterfaceType, stepPin4, dirPin4);
AccelStepper stepper5(motorInterfaceType, stepPin5, dirPin5);


AccelStepper* steppers[stepperAmount] ={
    
    &stepper0,
    &stepper1,
    &stepper2,
    &stepper3,
    &stepper4,
    &stepper5
};

void setup() {
	// set the maximum speed, acceleration factor,
	// initial speed and the target position
      for(int stepperNumber = 0; stepperNumber < stepperAmount; stepperNumber++){

        steppers[stepperNumber]->setMaxSpeed(100);
        steppers[stepperNumber]->setAcceleration(100);
        steppers[stepperNumber]->setSpeed(100);
        steppers[stepperNumber]->setCurrentPosition(0);
    }

  Serial.begin(9600);


}

void loop() {
//I commented out all the print statments we used for testing.
//steppers[0]->moveTo(100);

while (Serial.available() > 0 ) {
    char command = Serial.read();
    inputString += command;
    //Serial.print(command);
    if (command == '\n') {
      stringComplete = true;
      //Serial.print("Complete\n");
    }
    delay(10);
  }

  if (stringComplete) {
    //Serial.print("InsideComplete!\n");
    //Serial.print("first in"+inputString+"\n");
    stepNum = inputString.substring(0,2).toInt();
    //Serial.print("stepNum" + String(stepNum)+ "\n");
    //Serial.println(String(steppers[stepNum]->acceleration()));
    inputString = inputString.substring(1);
    //Serial.print("second in"+inputString+"\n");
    if (inputString.startsWith("F")) {
      //Serial.print("InsideF\n");
      int stepsToMove = inputString.substring(1).toInt();
      //Serial.print(String(stepsToMove)+ "\n");
      //Serial.println(String(steppers[stepNum]->acceleration()));
      steppers[stepNum]->moveTo(stepsToMove);
      steppers[stepNum]->runToPosition();
      steppers[stepNum]->setCurrentPosition(0);
      Serial.println("MOTOR_FINISHED");

    } else if (inputString.startsWith("S")) {
      steppers[stepNum]->stop();
      Serial.println("MOTOR_FINISHED");

    } else if (inputString.startsWith("R")) {
      //Serial.print("InsideR");
      steppers[stepNum]->moveTo(200);
      steppers[stepNum]->runToPosition();
      steppers[stepNum]->setCurrentPosition(0);
      Serial.println("MOTOR_FINISHED");

    } else if (inputString.startsWith("V")) {
      int speedStepper = inputString.substring(1).toInt();
      steppers[stepNum]->setSpeed(speedStepper);
      steppers[stepNum]->setMaxSpeed(speedStepper);
	    steppers[stepNum]->setAcceleration(speedStepper);
      Serial.println("MOTOR_FINISHED");

    } else if (inputString.startsWith("Q")) {
      Serial.print("MOTOR_CONNECTED");

    }
    
    inputString = "";
    stringComplete = false;
  }
  inputString = "";
  stringComplete = false;
}
