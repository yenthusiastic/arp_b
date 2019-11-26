//Using one of three possible power modes
#define NORMAL_MODE

//Enabling the Serial UART debug interface in order to check the I2C read/write commands
#define LIS3DH_DEBUG Serial

//Adding necessary libraries
#include "lis3dh-motion-detection.h"
#include "Wire.h"

int interruptPin = 27;                // Pin of the interrupt signal
int LIS3DH_ADDR = 0x18;               // I2C-Address of the IMU
int INT1_SRC_REG = 0x31;              // Interrupt1 register
int reading = 0;                      // Counting the amount of interrupts
volatile bool interruptFlag = false;  // Boolean flag
uint16_t sampleRate = 1;              // Samples per second -> 1 Hz
uint8_t accelRange = 4;               // Acceleration Range -> 4g

LIS3DH myIMU(0x18); // Initiating the IMU with the address 0x18

void setup() {
  Serial.begin(115200);
  delay(1000);

  // Starting the initiation and printing the status
  if( myIMU.begin(sampleRate, 1, 1, 1, accelRange) != 0) {
    Serial.print("Failed to initialize IMU.\n");
  } else {
    Serial.print("IMU initialized.\n");
  }

  uint8_t readData = 0;
 
  // Get the ID of the IMU: (0x33)
  myIMU.readRegister(&readData, LIS3DH_WHO_AM_I);
  Serial.print("Who am I? 0x");
  Serial.println(readData, HEX);

  init_ACC_ints(); // configuring the registers for the interrupts

  // Attaching the interrupt
  attachInterrupt(digitalPinToInterrupt(interruptPin), LISinterrupt, RISING);
  
}

void loop() {
  //  Count the amount of interrupts
  if (interruptFlag) {
    Serial.print("\t\tinterrupt: ");
    Serial.print(reading++);

    // Reading the register of the interrupt in order to latch it (otherwise it won't be resetted)
    uint8_t readData = 0;
    myIMU.readRegister(&readData, INT1_SRC_REG);
    
    Serial.print(",  ");
    Serial.println(interruptFlag);
    interruptFlag = false;
  }
  Serial.println();
  delay(50);
}

// Configurations of the IMU's registers
void init_ACC_ints(void) {
  myIMU.writeRegister(0x21, 0x09); // Activate the HPF
  myIMU.writeRegister(0x22, 0x40); // Enabling interrupt on INT1
  myIMU.writeRegister(0x23, 0x00); // Using full-scale mode
  myIMU.writeRegister(0x24, 0x00); // Activating latched interrupt requests
  myIMU.writeRegister(0x32, 0x06); // Interrupt threshold: 6LSBs * 31.25mg/LSB = 187mg.
  myIMU.writeRegister(0x33, 0x00); // Interrupt duration: 1LSBs * (1/10Hz) = 0.1s
  myIMU.writeRegister(0x30, 0x2A); // Enabling interrupt generations on all axis with a logical OR-Combination of interrupt events
  myIMU.writeRegister(0x20, 0x5F); // Activating all three axis including Low-Power mode (100Hz)
}

void LISinterrupt() {
  interruptFlag = true;
}
