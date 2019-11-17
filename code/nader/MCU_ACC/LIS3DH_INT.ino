//Using one of three possible power modes
#define NORMAL_MODE

//Enabling the Serial UART debug interface in order to check the I2C read/write commands
#define LIS3DH_DEBUG Serial

#include "lis3dh-motion-detection.h"
#include "Wire.h"

int interruptPin = 27;
int LIS3DH_ADDR = 0x18;
int INT1_SRC_REG = 0x31;
int reading = 0;
volatile bool interruptFlag = false;
uint16_t sampleRate = 1;
uint8_t accelRange = 4;

LIS3DH myIMU(0x18);

void setup() {
  Serial.begin(115200);
  delay(1000);

  if( myIMU.begin(sampleRate, 1, 1, 1, accelRange) != 0) {
    Serial.print("Failed to initialize IMU.\n");
  } else {
    Serial.print("IMU initialized.\n");
  }

  uint8_t readData = 0;
  
  // Get the ID:
  myIMU.readRegister(&readData, LIS3DH_WHO_AM_I);
  Serial.print("Who am I? 0x");
  Serial.println(readData, HEX);

  init_ACC_ints();

  attachInterrupt(interruptPin, LISinterrupt, RISING);
  
}

void loop() {
  if (interruptFlag) {
    Serial.print("\t\tinterrupt: ");
    Serial.print(reading++);
  
  uint8_t readData = 0;
  myIMU.readRegister(&readData, INT1_SRC_REG);
  Serial.print(",  ");
  Serial.println(interruptFlag);
    interruptFlag = false;
  }
  Serial.println();
  delay(50);
}


void init_ACC_ints(void) {
  myIMU.writeRegister(0x21, 0x09);
  myIMU.writeRegister(0x22, 0x40);
  myIMU.writeRegister(0x23, 0x00);
  myIMU.writeRegister(0x24, 0x00);
  myIMU.writeRegister(0x32, 0x06);
  myIMU.writeRegister(0x33, 0x00);
  myIMU.writeRegister(0x30, 0x2A);
  myIMU.writeRegister(0x20, 0x5F);
}

void LISinterrupt() {
  interruptFlag = true;
}
