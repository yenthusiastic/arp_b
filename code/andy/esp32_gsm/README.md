# esp32_gsm


### Module
 - **Name:**   LILYGO TTGO T-Call V1.3 ESP32 Wireless Module GPRS Antenna SIM Card SIM800L Board
 - **Link:**   [Product Page](https://www.banggood.com/LILYGO-TTGO-T-Call-V1_3-ESP32-Wireless-Module-GPRS-Antenna-SIM-Card-SIM800L-Board-p-1527048.html)
 - **Price:**   13 €   
 
![Pinout](/media/TTGO-T-call-Pinout.jpg)


### SIM Card
- Disable PIN
- lookup APN name, username and password: [apnchanger.org](https://wiki.apnchanger.org/Germany#Vodafone)
- Vodafone:
	- web.vodafone.de, vodafone, vodafone


## MircoPython and Example Code
[LoBo MicroPython for ESP32](https://github.com/loboris/MicroPython_ESP32_psRAM_LoBo/wiki)


[RTC Sync with NTP](https://github.com/loboris/MicroPython_ESP32_psRAM_LoBo/wiki/rtc)

[GSM Library](https://github.com/loboris/MicroPython_ESP32_psRAM_LoBo/wiki/gsm)


## Pin Mapping
|Pin ESP| Pin AUX|AUX Device|Protocol|Note|
|---    |---     |---       |---     |--- |
|3V3 	| | epaper, BME280E, Buzzer| | |
|5V 	| | MPU6050, [GPS, Co2, SDS011]| | |
|0 |BTN1 |Button1|GPIO digital |wake0 for deepsleep |
|2 |- |Buzzer |GPIO digital | pull-up at startup |
|4 |GSM_PWR |GSM Module |GPIO digital| |
|5 |GSM_RST |GSM Module |GPIO digital| |
|12 | Gate| Mosfet 5V (GPS, Co2, SDS011) |switched off in sleep | pull-down at startup |
|13 | | | |buildin LED |
|14 |INT |MPU6050 | | |
|15 |DIN |epaper| | |
|18 |PM10 |SDS011 Sensor |GPIO digital |Input: pulse length |
|19 |PM25 |SDS011 Sensor |GPIO digital |Input: pulse length |
|21 |SDA |MPU6050, BM260 |I2C | |
|22 |SCL |MPU6050, BM260 |I2C | |
|23 |GSM_MODEM_PWR |GSM Module |GPIO digital| |
|25 |CLK |epaper | | |
|26 |TX |GSM Module |Serial | |
|27 |RX |GSM Module |Serial | |
|32 |DC |epaper | | |
|33 |CS |epaper | | |
|34 |BUSY |epaper | |input only, no pulls|
|35 |TX |GPS |Serial |input only, no pulls |
|36/SVP |A0 |Co2 Sensor |GPIO analog|input only, no pulls |
|39/SVN |BAT | Battery Voltage |GPIO analog |input only, no pulls |


## Low power operation
The follwing action can be taken to reduce the overal system power consumption:
 - reduce core frequency from 240 MHz to 40 MHz
 - power off GSM module while not needed
 - disable power to connected sensors, if no adequate low-power mode is provided
     - some sensors like GPS can have a long cold-start time 

### Test results
See the tables below for power and timing test results.The GSM module can be powered down and up again without poblems. If the core frequency is reduced, the time to establish a GSM connection nearly triples at 60 seconds! Hence the startup core frequency of 240 MHz is kept till a connection is established.

Further tests revealed, that changing the frequency while the modem is online and making a HTTP request, renders the modem unresponsive to any commands till a hard reset is conducted. Therefore the core frequency has to be at 240 MHz while a request is made.

The following recommendations can be made:
 - For GSM connection a core frequency of 240 MHz is used
 - While the modem is online but no request is send, the frequency can be reduced to 40 MHz
 - Before any request is send, the frequency has to be set to 240 MHz
 - While the model is powered off, the frequency can be choosen freely.


#### Stats
##### Power
|State|Freq (MHz)|mA USB| mA Bat|V Bat|Wh Bat|
|---  |---       |---   |---    |---  |---   |
|Idle|240|27|32|3.57|0,1142|
|Idle|40|5|7|3.57|0,025|
|Idle & Modem Online|240|47|45|3.57|0,1607|
|Idle & Modem Online|40|-|19|3.57|0,0678|
|Deepsleep|all|-|0.130|3.57|0,0005|


##### Timing
|Function|Freq (MHz)|Time (sec)|
|---     |---       |---       |
|Connect GSM|240|22|
|Connect GSM|40|60|
|Get Balance|240|5|
|Get Balance|40|8|

#### Sensor Power
|Sensor Name| Voltage| Current reading| Current standby| Note|
|---        |---     |---    	      |---             |---  |
|DHT22 	    |3.3/ 5  | 1.38 mA        | 0.28 mA        | |
|GPS 	    |3.3/ 5  | 50 mA	      | NA	       | 70 mA peak|
|MPU6050    |5       | 5.4 mA	      | 0.05 mA	       | |
|BME280     |3.3     | 0.082 mA	      | NA	       | |
|MZ-14      |5       | 100 mA	      | 7.8 mA	       | |
|    |       | 0 mA	     | 0 mA	    | |


## Flash MicroPython
```bash
cd esp32_gsm/micropython_binaries/esp32_psram_all-custom
esptool.py --port /dev/ttyUSB4 erase_flash
esptool --chip esp32 --port /dev/ttyUSB4 --before default_reset --after no_reset write_flash -z --flash_mode dio --flash_freq 40m --flash_size detect 0x1000 bootloader/bootloader.bin 0xf000 phy_init_data.bin 0x10000 MicroPython.bin 0x8000 partitions_mpy.bin
```

## GSM Module Support
Currently (Q3 2019) MicroPython stable release (MPSR) supports PPP (GSM) in its network stack, but it is not implemented yet. Using the MPSR, the GSM module can only be used with *AT-commands* over the UART connection
. Because of that, the requests library can not be used to issue HTTP requests.

The GSM module (SIM800L) supports two ways of issuing requests. One is trough a direct TCP connection, but this mode doesn't support SSL encryption. Hence it can not be used to issue an IOTA-API call to an IOTA-Node.
The second way is trought usage of the builtin HTTP stack. The stack supports GET and PUT requests, but doesn't allow the HEADER and BODY of an request to be customized. Therefore it can not be used to to issue an IOTA-API call to an IOTA-Node.

In conclusion, the MPSR can not be used to interact with an IOTA-Node. Therefore the custom build MicroPython firmware by [loboris](https://github.com/loboris/MicroPython_ESP32_psRAM_LoBo/wiki/gsm) will be used for development of this project. Last commits to the repository were made in summer 2018. Because of this, it doesn't contain relevant functionalities with are implemented in the stable releases. These functionalities are:
 - deepsleep with wake-up source 
 - DHT22 library
Therefore the to be developed prototype might not be able to suport any low-power modes to enhace battery operation time. Additionaly a custom solution to interact with the DHT22 module has to be developed. 

## GSM Code
[Python Example SIM800](http://www.python-exemplary.com/index_en.php?inhalt_links=navigation_en.inc.php&inhalt_mitte=raspi/en/gsm.inc.php)


## Libraries Used
[QR-Code Generation](https://github.com/JASchilz/uQR)
[MPU6050](https://github.com/adamjezek98/MPU6050-ESP8266-MicroPython) (modified)
[BME280](https://github.com/robert-hh/BME280)
[E-Paper](https://github.com/mcauser/micropython-waveshare-epaper/blob/master/epaper2in9.py)


## Comiling Modules
[MicroPython cross compiler](https://github.com/micropython/micropython/tree/master/mpy-cross)
`python3 -m mpy_cross -v -mno-unicode -mcache-lookup-bc -march=xtensa epaper2in9.py`

Copy *.mpy file to ESP.

```bash
mpfshell
open ttyUSB1
put myfirmware.py main.py
```
