# esp32_gsm


# Hardware
## Development Board
[LILYGO TTGO T-Call V1.3 ESP32 Wireless Module GPRS Antenna SIM Card SIM800L Board](https://www.banggood.com/LILYGO-TTGO-T-Call-V1_3-ESP32-Wireless-Module-GPRS-Antenna-SIM-Card-SIM800L-Board-p-1527048.html)

 
![Pinout](/media/TTGO-T-call-Pinout.jpg)


## Components
### Minimum Required Hardware for Renting Operation						
|Component	| Details|
|---	|---	|
|Microcontroller & SIM Modem |LILYGO TTGO T-Call V1.3 ESP32 Wireless Module GPRS Antenna SIM Card SIM800L Board|
|GPS Module	| Beitian Dual BN-220 GPS GLONASS Antenna Module TTL Level RC Drone Airplane|
|Accelerometer	|LIS3DH Acceleration Sensor
|Display	|Waveshare 2.9 Inch E-Paper
|Voltage Converter	|Pololu 5V Step-Up Voltage Regulator U1V10F5
|Battery Charger & Protector	|TP4056 Micro USB 5V 1A Lithium Battery Charging Module
|Battery 	|Samsung - INR18650-35E - 3,6 Volt 3450mAh Li-Ion [LiNiCoAlO2]
|Batter Holder	|Battery Holder Plastic Case 4x 18650 Lithium Battery

### Additional Environmental Sensors																
|Component	| Details|
|---	|---	|
|Particulate Matter Sensor	|PM Sensor SDS011 High Precision Laser PM2.5 Air Quality Detection Sensor
|Temperature, Humidity & Pressure Sensor	|BME280 Digital Sensor Temperature Humidity Atmospheric Pressure
|CO2 Sensor	|NDIR CO2 Sensor MH-Z14A 0-5000PPM


## Pin Mapping
|Pin ESP| Pin AUX|AUX Device|Protocol|Note|
|---    |---     |---       |---     |--- |
|3V3 	| | ePaper, BME280, Buzzer| | |
|5V 	| | LIS3DH, [GPS, Co2, SDS011]| | |
|0 |BTN1 |Button1|GPIO digital |wake0 for deepsleep |
|2 |- |Buzzer |GPIO digital | pull-up at startup |
|4 |GSM_PWR |GSM Module |GPIO digital| |
|5 |GSM_RST |GSM Module |GPIO digital| |
|12 | Gate| Mosfet 5V (GPS, CO2, SDS011) |switched off in sleep | pull-down at startup |
|13 | | | |buildin LED |
|14 |INT |LIS3DH | | |
|15 |DIN |ePaper| | |
|18 |PM10 |SDS011 |GPIO digital |Input: pulse length |
|19 |PM25 |SDS011 |GPIO digital |Input: pulse length |
|21 |SDA |LIS3DH, BME280 |I2C | |
|22 |SCL |LIS3DH, BME280 |I2C | |
|23 |GSM_MODEM_PWR |GSM Module |GPIO digital| |
|25 |CLK |ePaper | | |
|26 |TX |GSM Module |Serial | |
|27 |RX |GSM Module |Serial | |
|32 |DC |ePaper | | |
|33 |CS |ePaper | | |
|34 |BUSY |ePaper | |input only, no pulls|
|35 |TX |GPS |Serial |input only, no pulls |
|36/SVP |A0 |CO2 Sensor |GPIO analog|input only, no pulls |
|39/SVN |BAT | Battery Voltage |GPIO analog |input only, no pulls |


# Software
## Which MicroPython?
Currently (Q3 2019) MicroPython stable release (MPSR) supports PPP (GSM) in its network stack, but it is not implemented yet. Using the MPSR, the GSM module can only be used with *AT-commands* over the UART connection
. Because of that, the requests library can not be used to issue HTTP requests as it requires an network interface.

The GSM module (SIM800L) supports two ways of issuing requests. One is trough a direct TCP connection, but this mode doesn't support SSL encryption. Hence it can not be used to issue an IOTA-API call to an IOTA-Node.
The second way is trought usage of the builtin HTTP stack. The stack supports GET and PUT requests, but doesn't allow the HEADER and BODY of an request to be customized. Therefore it can not be used to to issue an IOTA-API call to an IOTA-Node.

In conclusion, the MPSR currently can not be used to interact with an IOTA-Node. Therefore the custom build MicroPython firmware by [loboris](https://github.com/loboris/MicroPython_ESP32_psRAM_LoBo/wiki/gsm) will be used for development of this project. Last commits to the repository were made in summer 2018, which means it might not contain functionalities that are currently implemented in mainline MicroPython.

### Download MicroPython
[Loboris MicroPython Port Generic ESP32](https://github.com/loboris/MicroPython_ESP32_psRAM_LoBo/wiki/firmwares)
[Loboris Micropython Port for LILYGO TTGO T-Call](https://github.com/loboris/MicroPython_ESP32_psRAM_LoBo/raw/master/MicroPython_BUILD/firmware/MicroPython_LoBo_esp32_psram_all.zip)

## Flash MicroPython
[Instructions](https://docs.micropython.org/en/latest/esp8266/tutorial/intro.html#deploying-the-firmware)
```bash
cd esp32_gsm/micropython_binaries/esp32_psram_all-custom
esptool.py --port /dev/ttyUSB4 erase_flash
esptool --chip esp32 --port /dev/ttyUSB4 --before default_reset --after no_reset write_flash -z --flash_mode dio --flash_freq 40m --flash_size detect 0x1000 bootloader/bootloader.bin 0xf000 phy_init_data.bin 0x10000 MicroPython.bin 0x8000 partitions_mpy.bin
```
## Libraries

[LIS3DH](https://github.com/hdsjulian/micropov/blob/master/lis3dh.py) (modified)

[E-Paper](https://github.com/mcauser/micropython-waveshare-epaper/blob/master/epaper2in9.py)

[QR-Code Generation](https://github.com/JASchilz/uQR) 

[BME280](https://github.com/robert-hh/BME280)



## SIM Card Instructions
- Disable PIN
- lookup APN name, username and password: [apnchanger.org](https://wiki.apnchanger.org/Germany#Vodafone)
- Vodafone:
	- web.vodafone.de, vodafone, vodafone


