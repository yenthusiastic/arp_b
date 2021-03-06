## TODOs
### 3.1 Mobile connectivity
- [X] Implement connection to mobile network.
- [X] HTTP request trough mobile internet connection.
- [X] Mobile call a phone number (alarm mode).
- [X] Send SMS to phone number.
- [X] Read received SMS.

### 3.2.1. Peripherals - Sensor integration
- [X] Integrate GPS.
- [X] Integrate BME280E (humidity/temperature/pressure).
- [X] Integrate SDS011 (particulate matter). 
- [X] Integrate MPU6050 (accelerometer).
- [X] Integrate LIS3DH (accelerometer).
- [X] Integrate MH-Z14A CO2 sensor. 
- [X] Implement accelerometer interrupt signal for deep sleep wake up.
- [ ] Implement vibration measurement from accelerometer to detect if bike is parked and is not moving.




### 3.2.2. Peripherals - Human Machine Interface
- [X] Update Balance on status based intervalls
- [X] Generate and draw QR code.
- [ ] Add zero padding to all number outputs. 

### 3.3. Hardware implementation - Power System
- [X] Implement voltage conversion circuit.
- [X] Integrate solar charger in power system. 
- [X] Implement power MOSFET to disable sensors on 5V rail for deepsleep.

 

### 3.5. Firmware
- [X] Implement sleepmode with status.
- [X] Save QR code and IOTA address to RTC memory for deepsleep.
- [X] Read QR code and IOTA address from RTC memory after wakeup
- [X] Implement session management from wakeup to sleep.
- [X] Request IOTA address from server.



## Sensors

### GPS Sensor - [Beitian Dual BN-220 GPS](https://www.banggood.com/Beitian-Dual-BN-220-GPS-GLONASS-Antenna-Module-TTL-Level-RC-Drone-Airplane-p-1208588.html?rmmds=search&cur_warehouse=CN)
Price: 10€  
Interface: Serial

Supported GNSS: GPS,GLONASS,Galileo,BeiDou  
Provided data: data & time, latitude, longitude, altitude, number of received satelites, quality, speed_kmh, course (heading), [dop](https://gisgeography.com/gps-accuracy-hdop-pdop-gdop-multipath/)  
[Datasheet](https://files.banggood.com/2016/11/BN-220%20GPS+Antenna%20datasheet.pdf)



### Accelerometer/Gyroscope Sensor- [MPU-6050](https://www.banggood.com/6DOF-MPU-6050-3-Axis-Gyro-With-Accelerometer-Sensor-Module-For-Arduino-p-80862.html?rmmds=detail-top-buytogether-auto&cur_warehouse=CN)
6-DOF - 3-axis accelerometer and 3-axis gyroscope  
Price: 2€  
Interface: I2C  
[Datasheet](https://www.invensense.com/wp-content/uploads/2015/02/MPU-6000-Datasheet1.pdf)\
[Register Map](https://www.invensense.com/wp-content/uploads/2015/02/MPU-6000-Register-Map1.pdf)



### Temperature/ Humidity/ Atmospheric Pressure Sensor - [BME280E](https://www.banggood.com/BME280-Digital-Sensor-Temperature-Humidity-Atmospheric-Pressure-Sensor-Module-p-1354769.html?rmmds=search&cur_warehouse=CN)
Price: 4€  
Interface: I2C  
Data: temperature, relative humidity, atmosperic pressure (hPa)  
[Datasheet](https://ae-bst.resource.bosch.com/media/_tech/media/datasheets/BST-BME280-DS002.pdf)



### CO2 Sensor - [MH-Z14A](https://www.banggood.com/NDIR-CO2-Sensor-MH-Z14A-PWM-NDIR-Infrared-Carbon-Dioxide-Sensor-Module-Serial-Port-0-5000PPM-Controller-p-1248270.html?rmmds=search&cur_warehouse=CN)  
Price: 20 €  
Interface: Analog DC Voltage 
Data: Air Co2 concentration in parts-per-million (PPM)
[Datasheet](http://myosuploads3.banggood.com/products/20190729/20190729034710mh-z14co2.pdf)



### Particulate Matter (PM)/ Fine Dust Sensor - [Nova SDS011](https://www.banggood.com/Geekcreit-Nova-PM-Sensor-SDS011-High-Precision-Laser-PM2_5-Air-Quality-Detection-Sensor-Module-Tester-p-1144246.html?rmmds=search&cur_warehouse=CN)
Price: 20€  
Interface: PWM  
The SDS011 is using the principle of laser scattering to measure the concentration of particles of a size between 0.3 to 10 µm. Resolution of 0.3µg/m³.  
Power consumtion:
  - Running 70 mA
  - Sleep 3mA  
[Datasheet](https://cdn-reichelt.de/documents/datenblatt/X200/SDS011-DATASHEET.pdf)



### [NOT USED ANYMORE] ~Humidity and Temperature Sensor - [ASAIR AM2302 (DHT22)](https://www.banggood.com/AM2302-DHT22-Temperature-And-Humidity~-Sensor-Module-For-Arduino-SCM-p-937403.html?rmmds=detail-top-buytogether-auto&cur_warehouse=CN)~
Price: 3.5 €  
Interface: 1-wire  
[Datasheet](https://cdn-shop.adafruit.com/datasheets/Digital+humidity+and+temperature+sensor+AM2302.pdf)






