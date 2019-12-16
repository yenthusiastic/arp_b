# PCB development
This readme is going to describe the process of the PCB development. 
It is including the installation and configuration of KiCAD, the electrical and mechanical requirements for the PCB and the design process itself.

## Ideas & plans
The idea of this task is to develop a PCB, which is electrically connecting the single components (MCU, sensors, etc.) together. Most of the sensors are soldered on breakout boards, which include all electrical components necessary for a standard operation. These components are for example resistors, capacitors and/or voltage regulators. Most of the time, a pin header is also included in order to connect the sensor to the MCU using jumper wires.
Breakout boards have also the advantage, that they implicate a very good documentation and that they are easily reusable.
Of course, it is also possible to have a closer look at the breakout boards and use all the necessary components on the main PCB, which is going to be developed. But in order to reduce complexity and the time-stress-level, a PCB using the breakout boards is the way to go.

## Researches

### KiCAD vs. Eagle
The first decision to make is the question of the right PCB design software. The discussions are most of the time endless, but in the end, it is a question of personal preference, as both softwares have their advantages and disadvantages.

#### Price
KiCAD is free and open-source, which means that is possible to download the complete source code and modify it ad libitum. At the other side, EAGLE is available as a free version, but it is restricting the complexity of the projects by three different limitations:
* maximum of two layers
* maximum of two schematics sheets
* maximum of 80 cm² board size

It is also possible to use the full version of EAGLE, but it either costs 17.85 EUR monthly or 130.90 EUR yearly.

#### User interface / User experience
The user interfaces of both softwares are optically not feauturing any major differences, but in terms of user experience, KiCAD is one step ahead by including standard keyboard shortcuts for the different main tools you use when designing a PCB. With Eagle it is possible to use shortcuts, but with the difference, that they have to be configured first. Nevertheless, EAGLE is featuring a command line, where it is possible to type in commands (e.g. wire, place component, etc.). EAGLE's main advtange is that the process of developing a PCB is much more straight-forward, as it takes less steps:
1. Create a schematic
2. Place components. (Here, each time you place a component, you already define the type of footprint you want to choose)
3. Connect the components (circuit)
4. Generate board (one click and the components are placed on the edge of the board)
5. Final placements and connections are made (Changes in the schematics are directly copied in the board)

KiCad involves a few more steps, but after executing these steps multiple times, it does not make a difference. The difference is more decisive for a new-comer.
* The footprints of the components are selected after placing all the components in the schematic.
* Components are not directly named when getting placed
* The process of getting the components and connections to the board involves two more steps
    * Create a netlist
    * Load netlist into the board

#### Components organization
In every PCB design software, each single component is including a *footprint* and a *symbol*; KiCAD and EAGLE are not making any exceptions. The symbol is used when the component is placed in one of the schematics sheets, where rotation and position are not playing any roles. It is only important, that the component is placed and connected to the other components with the *wire tool*. As soon as the schematics are finished, it is time to place the footprint of the component. Here, the position as well as the roation are crucial, as the component is going to be soldered (or fixed) exactly how it is placed in the *Gerber files* (output files of the PCB).
Both softwares have a libary, where you can manage the symbols as well as the footprints, but in my opinion, the one of EAGLE is much more easier to handle. KiCAD is a little bit more complicated (as you can see under *Problems & Troubleshooting*).

### Components
* [LIS3DH](https://www.st.com/resource/en/datasheet/lis3dh.pdf) - Acceleration sensor
* [VIS3590](https://www.reichelt.de/12-mm-magnetischer-buzzer-vis-3590-p248314.html?PROVID=2788&gclid=Cj0KCQiAk7TuBRDQARIsAMRrfUZGc0MFfkMijM4triyhI70YJm8uVk0_bFY5iUcvsQDlfDWVVrutPQUaAqmwEALw_wcB&&r=1) - Buzzer
* [MH-Z14A](https://www.banggood.com/de/NDIR-CO2-Sensor-MH-Z14A-PWM-NDIR-Infrared-Carbon-Dioxide-Sensor-Module-Serial-Port-0-5000PPM-Controller-p-1248270.html?gmcCountry=DE&currency=EUR&createTmp=1&utm_source=googleshopping&utm_medium=cpc_bgs&utm_content=frank&utm_campaign=frank-ssc-de-css-all-19bf11&ad_id=380597671089&gclid=Cj0KCQiAk7TuBRDQARIsAMRrfUZKyH9uKiOI8AsN_9JS3UmNfRLCO_lH9K2vEJEZapdY7mxqP0jCGBUaArfyEALw_wcB&cur_warehouse=CN) - CO₂ sensor
* [BN220](https://www.banggood.com/de/Beitian-BN-220T-GPS-GLONASS-Module-For-APM-Pixhawk-CC3D-Naze32-F3-F4-Flight-Controller-RC-Drone-Airplane-p-1446169.html?gmcCountry=DE&currency=EUR&createTmp=1&utm_source=googleshopping&utm_medium=cpc_bgs&utm_content=frank&utm_campaign=ssc-de-all-0716&ad_id=367212437657&gclid=Cj0KCQiAk7TuBRDQARIsAMRrfUZp8J6SOXBwY3z7kkAh3ZLmuUUmqHAU2cbT82qMtKNmgjt5V-ikGVwaArADEALw_wcB&cur_warehouse=CN) - GPS sensor
* [SDS011](https://www.banggood.com/de/Geekcreit-Nova-PM-Sensor-SDS011-High-Precision-Laser-PM2_5-Air-Quality-Detection-Sensor-Module-Tester-p-1144246.html?gmcCountry=DE&currency=EUR&createTmp=1&utm_source=googleshopping&utm_medium=cpc_bgs&utm_content=frank&utm_campaign=frank-ssc-de-css-all-19bf11&ad_id=380597671089&gclid=Cj0KCQiAk7TuBRDQARIsAMRrfUaDJpclHDIj_aa5fgJSP1aEasOmDeB9t93sI-2GWzTbn4nR9yIGIDQaAoamEALw_wcB&cur_warehouse=CN) - PM sensor
* [RND 135-00180](https://www.reichelt.de/led-smd-0603-blau-200-mcd-rnd-135-00180-p263776.html?&trstct=pol_8) - Status LED
* [BME280](https://www.reichelt.de/entwicklerboards-temperatur-feuchtigkeits-und-drucksensor-debo-sens-thd-p235476.html?&trstct=pos_2) - Temperature, pressure and humidity sensor


## Development of the PCB
In this part, the hardware implementation is going to be outlined. In general, it is the part of the project where all modules with all necessary components are going to be connected to each other on one single place.

### Results
The PCB v0.1 has a final size of 83.69mm by 78.11mm. All sensors are connected to the microcontroller via the PCB, but as all environmental sensors are only used as soon as the bicycle is in use, they are switched on by a mosfet in order to save power. In addition, all the environmental sensors are connected via jumper cables to the board, due to the mounting on the housing because of airflow. 

#### Schematics
The following figure is showing the final schematics of the PCB in version 0.1. 

<p align="center">
  <img src="https://raw.githubusercontent.com/yenthusiastic/arp_b/master/code/nader/PCB/img/Schematics.png" width="90%" title="Schematics" alt="Image of the schematics">
</p>
</br>

The big part in the middle of the schematic is the microcontroller (ESP32) itself. As this PCB is still some kind of a prototype, we have placed socket connector strips next to the connections of the MCU itself in order to have a direct access to all the necessary pins when debugging is necessary. The jumper JP6 is connected to a resistor, which is then directly connected to ground and used for a potential LED. The few components above the microcontroller are used for the buzzer, which is giving an accousting feedback whenever the device is swiched on. Additionally, it can be used to give a general accoustic feedback for different kinds of situations. The three components to the right of the MCU are the three environmental sensors. Above is the measuring the temperature, humidity and the pressure, while the middle one is the CO₂ sensor and below is the sensor used for the measurement of particulate matter in the air. The component in the lower right corner is the ePaper-module, which is displaying the QR-code and general information about the rental itself. Below of the MCU is a voltage divider, which is sent to the sensVN pin of the microcontroller. In the lower left corner is the circuit of the mosfet, which is switching the three environmental sensor on and off. The first component above the mosfet circuit is the voltage regulator including the power socket, which is providing the board with 5V with an input voltage of 3-5V. The GPS module is seen above the voltage regulator, while the last component in the upper left corner is the acceleration sensor itself. The accelerometer is the only sensor, which is soldered directly on the board instead of a connection via jumper wires. 

#### Layout
Once the schematics are finished, the PCB itself has to be designed. All connections are already defined, so it is necessary to place all components in a smart way in order to prevent long traces between two components and also route these traces. The figure below is showing the initial look of the PCB as soon as the file board is generated by the schematics. The yellow lines between the components are representing necessary connections, which have to be routed. In general one can say, that the more chaotic the lines are, the more chaotic is going to be the final routing. 
The first step is to place the components to their final positions, which is shown in the image below. The black area is representing the current dimensions of the PCB. Here, it is very helpful to first group components together. For example, in the schematics it can be seen that the circuit of the mosfet is including the transistor itself, three resistors and an LED. This means, that these components are at the best placed right next to each other. Another example are the spcker connector strips; These have to be placed next to the microcontroller, as its pins are directly connected to those of the sockets. 
<p align="center">
  <img src="https://raw.githubusercontent.com/yenthusiastic/arp_b/master/code/nader/PCB/img/Board01.png" width="90%" title="Board: Step 1" alt="Image of the Board: Step 1">
</p>
</br>

The next figure is showing the PCB after the components have been placed. The power is coming through the connector in the upper left corner. The modules and sensors are placed corresponding to the position of the microcontroller's pins. That's why the ePaper display, the CO₂-Sensor and the GPS module are placed on one side, and the others (Accelerometer, PM-sensor, environmental-sensor and buzzer) are placed on the other side. Furthermore, the mounting houles of the PCB itself have also been placed in the four corners, which fit 3mm mounting screws. 
<p align="center">
  <img src="https://raw.githubusercontent.com/yenthusiastic/arp_b/master/code/nader/PCB/img/Board02.png" width="60%" title="Board: Step 2" alt="Image of the Board: Step 2">
</p>
</br>

The following figure is illustrating the status of the board after the final step. 
<p align="center">
  <img src="https://raw.githubusercontent.com/yenthusiastic/arp_b/master/code/nader/PCB/img/Board03.png" width="60%" title="Board: Step 3" alt="Image of the Board: Step 3">
</p>
</br>

### Problems & Troubleshooting
Test
