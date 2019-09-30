# esp32_gsm


### Module
 - **Name:**   LILYGO TTGO T-Call V1.3 ESP32 Wireless Module GPRS Antenna SIM Card SIM800L Board
 - **Link:**   [Product Page](https://www.banggood.com/LILYGO-TTGO-T-Call-V1_3-ESP32-Wireless-Module-GPRS-Antenna-SIM-Card-SIM800L-Board-p-1527048.html)
 - **Price:**   13 €   
 
![Pinout](/media/TTGO-T-call-Pinout.jpg)


### SIM Card
- Disable PIN
- lookup APN name, username and password: [apnchanger.org](https://wiki.apnchanger.org/Germany#Vodafone)


## MircoPython and Example Code
[Github - Xinyuan-LilyGO](https://github.com/Xinyuan-LilyGO/TTGO-T-Call/tree/master/examples/MicroPython_LoBo)


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



## Flash MicroPython
```bash
cd esp32_gsm/micropython_binaries/esp32_psram_all-custom
esptool.py --port /dev/ttyUSB4 erase_flash
esptool --chip esp32 --port /dev/ttyUSB4 --before default_reset --after no_reset write_flash -z --flash_mode dio --flash_freq 40m --flash_size detect 0x1000 bootloader/bootloader.bin 0xf000 phy_init_data.bin 0x10000 MicroPython.bin 0x8000 partitions_mpy.bin
```
