import urequests as requests
import json
import esp32, machine
from time import sleep_ms, sleep, ticks_ms,  ticks_diff
import time
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import mpu6050 as mpu

i2c = I2C(-1, Pin(4),Pin(5),freq=40000) # Bitbanged I2C bus
screen = SSD1306_I2C(128, 64, i2c)
screen.invert(1) # White text on black background

i2c_mpu = I2C(-1, scl=Pin(15), sda=Pin(13),freq=40000)
mpu.init_sensor(i2c_mpu, Pin(15), Pin(13))


btn = Pin(0, Pin.IN)

int0 = Pin(25, Pin.IN, Pin.PULL_UP)
esp32.wake_on_ext0(pin=int0, level=esp32.WAKEUP_ANY_HIGH)

def go_sleep():
    print('Im awake. Going to sleep in 3 seconds')
    sleep(3)
    print('Going to sleep now')
    machine.deepsleep()


def print_int_pin():
    print(interruptPin.value())  


UPDATE_INTERVAL = 2000

addr = mpu.i2c_test()
addr = str(addr).strip('[]')



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


def get_interrupt():
    print(mpu.get_interrupt_status())
   
   
   ###
    
motion = False

def handle_interrupt(pin):
    global motion
    motion = True
    global interrupt_pin
    interrupt_pin = pin
    
acc = Pin(14, Pin.IN)

acc.irq(trigger=Pin.IRQ_RISING, handler=handle_interrupt)


    

#connect_wifi(c.ssid, c.psk)
#dht = read_dht()
#screen.text("Temperature: {}".format(dht[0]),0,0,0)
#screen.text("Humidity: {}".format(dht[1]),0,20,0)
#screen.show()

try:
    screen.fill(1)
    screen.text("Hello!",0,30,0)
    screen.text(addr,0,20,0)
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
        
        if motion:
            print('Motion detected!')
            motion = False
        
except Exception as e:
        print("Exception at main: ", e)




