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


## Power
|State|Freq (MHz)|mA|
|---     |---       |---       |
|Idle|240|27|
|Idle|40|5|
|Idle & Modem Online|240|40|
|Idle & Modem Online|40|-|


## Timing
|Function|Freq (MHz)|Time (sec)|
|---     |---       |---       |
|Connect GSM|240|22|
|Connect GSM|40|60|
|Get Balance|240|5|
|Get Balance|240|8|

