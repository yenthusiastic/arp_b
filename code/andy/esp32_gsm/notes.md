# References
## GSM Code
[Python Example SIM800](http://www.python-exemplary.com/index_en.php?inhalt_links=navigation_en.inc.php&inhalt_mitte=raspi/en/gsm.inc.php)





## MircoPython and Example Code
[LoBo MicroPython for ESP32](https://github.com/loboris/MicroPython_ESP32_psRAM_LoBo/wiki)


[RTC Sync with NTP](https://github.com/loboris/MicroPython_ESP32_psRAM_LoBo/wiki/rtc)

[GSM Library](https://github.com/loboris/MicroPython_ESP32_psRAM_LoBo/wiki/gsm)


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





## Comiling Modules
[MicroPython cross compiler](https://github.com/micropython/micropython/tree/master/mpy-cross)
`python3 -m mpy_cross -v -mno-unicode -mcache-lookup-bc -march=xtensa epaper2in9.py`

Copy *.mpy file to ESP.

```bash
mpfshell
open ttyUSB1
put myfirmware.py main.py
```
