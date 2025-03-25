// Include the AccelStepper Library
#include <AccelStepper.h>
#include <EEPROM.h>  // For storing position

//Defining the amount of steppers
const int stepperAmount = 6;

// Define pin connections
const int dirPins[stepperAmount] = {2, 4, 6, 8, 10, 12};
const int stepPins[stepperAmount] = {3, 5, 7, 9, 11, 13};

String inputString = "";
boolean stringComplete = false;
int stepNum = 1;

#define motorInterfaceType 1

// Stepper motor instances
AccelStepper* steppers[stepperAmount];

// Motor configuration
int currentPosition[stepperAmount];
int maxPosition[stepperAmount] = {6000, 0, 0, 0, 0, 0}; // 0 = no limit

void setup() {
  Serial.begin(9600);

  // Initialize steppers
  for (int i = 0; i < stepperAmount; i++) {
    steppers[i] = new AccelStepper(motorInterfaceType, stepPins[i], dirPins[i]);
    steppers[i]->setMaxSpeed(100);
    steppers[i]->setAcceleration(100);
    steppers[i]->setSpeed(100);

    // Load position from EEPROM
    EEPROM.get(i * sizeof(int), currentPosition[i]);
    steppers[i]->setCurrentPosition(currentPosition[i]);
  }
}

void loop() {
  while (Serial.available() > 0) {
    char command = Serial.read();
    inputString += command;
    
    if (command == '\n') {
      stringComplete = true;
  
    }
    delay(10);
  }

  if (stringComplete) {
    stepNum = inputString.substring(0, 2).toInt();
    inputString = inputString.substring(1);

    if (inputString.startsWith("S")) {
      steppers[stepNum]->stop();
      Serial.println("MOTOR_FINISHED");

    } else if (inputString.startsWith("Q")) {
      Serial.print("MOTOR_CONNECTED");

    } else if (inputString.startsWith("V")) {
      int speedStepper = inputString.substring(1).toInt();
      steppers[stepNum]->setSpeed(speedStepper);
      steppers[stepNum]->setMaxSpeed(speedStepper);
      steppers[stepNum]->setAcceleration(speedStepper);
      Serial.println("MOTOR_FINISHED");
    
    } else if (inputString.startsWith("M")) {
      int relativeOffset = inputString.substring(1).toInt();
      int relativeTarget = currentPosition[stepNum] + relativeOffset;
      moveMotor(stepNum, relativeTarget);

    } else if (inputString.startsWith("A")) {
      int absoluteTarget = inputString.substring(1).toInt();
      moveMotor(stepNum, absoluteTarget);

    } else if (inputString.startsWith("H")) {  // Manually set home position
      setHome(stepNum);
    }

    inputString = "";
    stringComplete = false;
  }
}

void moveMotor(int motorIndex, int target) {
  if (maxPosition[motorIndex] > 0) {
    if (target > maxPosition[motorIndex]) {
      Serial.println("WARNING: Target above maxPosition. Moving to maxPosition instead.");
      target = maxPosition[motorIndex];
    } else if (target < 0) {
      Serial.println("WARNING: Target below 0. Moving to position 0 instead.");
      target = 0;
    }
  }

  steppers[motorIndex]->moveTo(target);
  steppers[motorIndex]->runToPosition();
  currentPosition[motorIndex] = target;
  EEPROM.put(motorIndex * sizeof(int), target);
  Serial.println("MOTOR_FINISHED");
}

void setHome(int motorIndex) {
  steppers[motorIndex]->setCurrentPosition(0);
  currentPosition[motorIndex] = 0;
  EEPROM.put(motorIndex * sizeof(int), 0);
  Serial.println("HOME_SET");
}

