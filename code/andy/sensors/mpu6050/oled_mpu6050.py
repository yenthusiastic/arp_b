import credentials as c
import urequests as requests
import json
from time import sleep_ms, sleep, ticks_ms,  ticks_diff
import time
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import mpu6050 as mpu

i2c = I2C(-1, Pin(4),Pin(5),freq=40000) # Bitbanged I2C bus
screen = SSD1306_I2C(128, 64, i2c)
screen.invert(1) # White text on black background

i2c_mpu = I2C(-1, scl=Pin(15), sda=Pin(13),freq=40000)
#i2c = I2C(0, I2C.MASTER, scl=Pin(22), sda=Pin(21), freq=400000)
mpu.init_sensor(i2c_mpu, Pin(15), Pin(13))


btn = Pin(0, Pin.IN)


UPDATE_INTERVAL = 2000


def read_mpu():
  try:
    
    #if (isinstance(temp, float) and isinstance(hum, float)) or (isinstance(temp, int) and isinstance(hum, int)):
    #  msg = (b'{0:3.1f},{1:3.1f}'.format(temp, hum))
    #  hum = round(hum, 2)
    return mpu.get_values()
    #else:
    #  return None #('Invalid sensor readings.')
  except OSError as e:
    print('Failed to read sensor: ', e)
    return None



#connect_wifi(c.ssid, c.psk)
#dht = read_dht()
#screen.text("Temperature: {}".format(dht[0]),0,0,0)
#screen.text("Humidity: {}".format(dht[1]),0,20,0)
#screen.show()

try:
    screen.fill(1)
    screen.text("Hello!",0,30,0)
    screen.show()
    last_print = time.ticks_ms()
    screen.show()
    while True:
        if btn.value() == 0:
            break
        cur_print = time.ticks_ms()
        cur_req = time.ticks_ms()
        
        if time.ticks_diff(cur_print, last_print) >= UPDATE_INTERVAL:
            last_print = cur_print
            print("Update sensor data...")
            mmt = read_mpu()
            screen.fill(1)

            screen.text("Temp: {:.2f} C".format(mmt[0]),0,20,0)
            screen.text("Hum: {:.2f} %".format(mmt[1]),0,30,0)
            screen.text("hPa: {:.2f} %".format(mmt[2]),0,40,0)
            screen.show()
            print("Sensor data: {}, {}, {}".format(mmt[0], mmt[1], mmt[2]))
        
except Exception as e:
        print("Exception at main: ", e)




