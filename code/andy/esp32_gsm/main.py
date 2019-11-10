'''
  MicroPython fork by loboris:
  https://github.com/loboris/MicroPython_ESP32_psRAM_LoBo/
'''

# ===== CONFIG ========

# APN Credentials
GSM_APN  = 'web.vodafone.de'
GSM_USER = 'vodafone'
GSM_PASS = 'vodafone'

# Module Settings
HARDWARE_ID = 1
API_KEY = "2ed617ed018c0b13f209fc0bbe75ab8ab1a1d303"
PHONE_NUMBER = '+491745851814'
SERVER_URL = "https://req.dev.iota.pw/"
NODE_URL2 = "https://nodes.iotadev.org/"
NODE_URL = "https://nodes.thetangle.org/"

UPDATE_INV = 1000

RENT_TIME_FACTOR = 1

# dev-strings
json_data = [{"hardwareID": 1}, {"vbat": 3850}]

m_address = "SVJQSVYGFUYZHKSQD9OYGSEMCSAWKNXEXMGJSUKQHHDYPDDOTVXYCHFWEAOCZUVOQFANVVLIDAPOTIDY9UCQYMMMXX"
m_states = {"offline": 0, "parked":1, "rented":2, "broken":3, "stolen":4}

DEBUG = True
# ===================


status = 0
status_old = 0
qr_display = 0
session_address = ""
session_balance = 0
session_start = 0
session_rent_time = 0


import machine, sys 
from machine import Pin, ADC, UART, I2C, GPS, DHT, RTC, deepsleep
import gsm
import socket
import urequests as requests
import json
from time import sleep, sleep_ms, ticks_ms, ticks_diff, time

import mpu6050 as mpu
import bme280_no_hum as bme280_float
import sds011

rtc = RTC()


status_def = {
    0:"Undefined",
    1:"Sleeping",
    2:"Updating Balance",
    3:"Session running",
    4:"Session over!",
    5:"BROKEN",
    6:"ALARM",
    7:"Offline"
}


# Setup GSM Module Pins
GSM_PWR = Pin(4, Pin.OUT)
GSM_RST = Pin(5, Pin.OUT)
GSM_MODEM_PWR = Pin(23, Pin.OUT)
#GSM_PWR.value(0)
#GSM_RST.value(0)
#GSM_MODEM_PWR.value(0)

# Setup User IO Pins
#LED = Pin(13, Pin.OUT)
#LED.value(1)

BTN1 = Pin(0, Pin.IN, Pin.PULL_UP)
LED = Pin(13, Pin.OUT, value=0)

# wake-up source for deepsleep
rtc.wake_on_ext0(pin=BTN1, level=0)

# MOSFET for 5V AUX
mos = Pin(12, Pin.OUT, value=0)

# Alarm Buzzer
buz = Pin(2, Pin.OUT, value=1)

# CO2 sensor, MH-Z14
adc=ADC(Pin(36))

# GPS
# RX is not used
gps = GPS(UART(2, rx=35, tx=33, baudrate=9600, bits=8, parity=None, stop=1, timeout=1500, buffer_size=1024, lineend='\r\n'))
gps.startservice()


# PM sensor, SSD011
PM10_PIN = Pin(19, Pin.IN)
PM25_PIN = Pin(18, Pin.IN)


# I2C
i2c = I2C(0, I2C.MASTER, scl=Pin(22), sda=Pin(21), freq=400000)

# accelerometer/ gyroscope, MPU6050
mpu.init_sensor(i2c)

# temperature/ humidity/ atmosperic pressure, BME280
bme = bme280_float.BME280(i2c=i2c)




# ===== DISPLAY ========
from machine import Pin, SPI
#import epaper2in9b_mod as epaper2in9b
import epaper2in9

spi = SPI(2, baudrate=2000000, polarity=1, phase=0, sck=Pin(25), mosi=Pin(15), miso=Pin(0))
BTN1 = Pin(0, Pin.IN, Pin.PULL_UP)

dc=Pin(32)
rst=Pin(14)
busy=Pin(34)
cs=Pin(33)

black = 0
white = 1

w = 128
h = 296
x = 0
y = 0

import framebuf
buf = bytearray(w * h // 8)
fb = framebuf.FrameBuffer(buf, w, h, framebuf.MONO_HLSB)
fb.fill(white)

e=epaper2in9.EPD(spi, cs, dc, rst, busy)
e.init()

def draw_title():
    fb.fill_rect(0,0,w,10, black)
    fb.text("B I K O T A", 20, 3, white)
    #e.draw_filled_rectangle(buf, 0,10,127,11, True)
    #e.draw_filled_rectangle(bufy, 0,15,127,168, True)
    fb.fill_rect(0,10,w,3, black)
    fb.fill_rect(0,35,w,3, black)

def draw_status(stat="Undefined", xs=0, ys=20):
    fb.fill_rect(0, ys-6, w, 21, white)
    if xs >= 0:
        if xs == 0:
            xs = int((w - (len(stat) * 8)) / 2) 
        fb.text(str(stat), xs, ys, black)

def draw_date(xs=0, ys=45):
    if rtc.now()[0] != 1970:
        fb.fill_rect(0, ys, xs+64, 11, white)
        if xs>=0:
            dt=rtc.now()[:6]
            fb.text("{}.{}.{}".format(dt[2], dt[1], dt[0]-2000), 0, ys, black)



def draw_balance(iota=session_balance, xs=0, ys=100):
    fb.fill_rect(0, ys, w, 8, white)
    if iota >= 0:
        fb.text("Balance: {}i".format(iota), 0, ys, black)
    #fb.fill_rect(0,ys+8,127,11, 1)
    #fb.text("{} i".format(iota),0,  ys+10, 0)

def draw_rent_time(xs=0, ys=120):
    global status, status_old, session_rent_time, session_balance, session_start
    status = status
    status_old = status_old
    session_rent_time= session_rent_time
    session_balance = session_balance
    session_start = session_start
    fb.fill_rect(0, ys, w, 8, white)
    if xs >= 0:
        if session_start > 0:
            session_rent_time = session_balance * RENT_TIME_FACTOR * 60
            delta = int(time()) - session_start
            if delta > session_rent_time and status == 3:
                status_old = status
                status = 4
                end_of_session_sound()
            if status == 3:
                s_delta = session_rent_time - delta
                dmin = int(s_delta // 60)
                dsec = int(s_delta % 60)
                fb.text("Session: {}:{}".format(dmin, dsec), 0, ys, black)
            elif status == 4:
                fb.text("Session over!", 0, ys, black)
                

def update_display():
    e.set_frame_memory(buf, x, y, w, h)
    e.display_frame()

def clear_buf(color = white):
    fb.fill_rect(0, 0, w, h, color)

def draw_qr(m=None, address=None, xs=2, ys=170, scale=1):
    fb.fill_rect(xs, ys, w, h-ys, white)   # clear QR area with white fill
    if m == None:
        if address == None:
            address = m_address_chsum
        m = make_qr(address) 
    for y in range(len(m)*scale):
        for x in range(len(m[0])*scale):
            value = m[y//scale][x//scale]
            if value == 0:
                value=0xFF
            else:
                value=0x00
            fb.pixel(xs+x, ys+y, value)

#========== /DISPLAY =================


def make_qr(address=m_address):
    if DEBUG: print("Making QR code...")
    from uQR import QRCode
    qr=QRCode(border=0)
    qr.add_data(address)
    m_address_matrix = qr.get_matrix()
    if DEBUG: print("QR code created.")
    return m_address_matrix


def checkms(t):
    while t.value()==0:
        start=ticks_ms()
    while t.value()==1:
        stop=ticks_ms()
    if DEBUG: print("Pulse:", (stop-start)-2)


def get_pm(p10=PM10_PIN, p25=PM25_PIN):
    while p10.value() !=0:
        sleep_ms(1)
    while p10.value() == 0:
        st_10=ticks_ms()
    while p10.value() == 1:
        sp_10=ticks_ms()
    while p25.value() !=0:
        sleep_ms(1)
    while p25.value() == 0:
        st_25=ticks_ms()
    while p25.value() == 1:
        sp_25=ticks_ms()
    if DEBUG: print("PM10:", (sp_10-st_10)-2)
    if DEBUG: print("PM25:", (sp_25-st_25)-2)



def get_co2():
    ppm = 0
    av_mv = 0
    if adc.progress()[0] == False:
        av_mv = adc.collected()[2]
        adc.collect(1, len=10, readmv=True)
        ppm = ((av_mv-400)/1600)*5000
        if ppm < 350:
            ppm = 0
    return ppm, av_mv


def get_bme():
  try:
    temp, hpa, _ = bme.values
    #temp, hpa, hum = bme.values
    #if (isinstance(temp, float) and isinstance(hum, float)) or (isinstance(temp, int) and isinstance(hum, int)):
    #  msg = (b'{0:3.1f},{1:3.1f}'.format(temp, hum))
    #  hum = round(hum, 2)
    #return temp, hum, hpa
    return temp, hpa
    #else:
    #  return None #('Invalid sensor readings.')
  except OSError as e:
    print('Failed to read sensor: ', e)
    return None

    

def gps_location():
    data = gps.getdata()
    if gps.getdata()[0][0] != 1900:
        return (data[1], data[2])
    else:
        return False


def gsm_connect():
    global gsm
    if gsm.status()[0] is 98 : # 98-not started; 89-idle; 0-disconnected
        if DEBUG: print("Power up GSM modem...")
        gsm.debug(True)
        #freq(240000000)
        GSM_PWR.value(1)
        sleep(0.1)
        GSM_PWR.value(0)
        GSM_RST.value(1)
        GSM_MODEM_PWR.value(1)
        sleep(1.1)
        GSM_PWR.value(1)
        sleep(0.3)
    if gsm.status()[0] is 98 or 89 or 0:
        gsm.start(tx=27, rx=26, apn=GSM_APN, user=GSM_USER, password=GSM_PASS)
        if DEBUG: sys.stdout.write('Waiting for AT command response...')
        for retry in range(50):
            if gsm.atcmd('AT'):
                break
            else:
                if DEBUG: sys.stdout.write('.')
                sleep_ms(500)
        else:
            raise Exception("Modem not responding!")
        if DEBUG: print()
        if DEBUG: print("Connecting to GSM...")
        gsm.connect()
        while gsm.status()[0] != 1:
            sys.stdout.write('.')
            sleep_ms(10)
            #pass
        print('IP:', gsm.ifconfig()[0])
        if rtc.now()[0] == 1970:
            if DEBUG: print("Update RTC from NTP server...")
            rtc.ntp_sync(server="hr.pool.ntp.org", tz="CET-1CEST")
            if DEBUG: print("RTC updated.")


def gsm_online_check(connect=False):
    if gsm.status()[0] == 1:
        return True
    else:
        if connect:
            gsm_connect()
            return True
        else:
            return False


def gsm_shutdown():
    if gsm.stop():
        GSM_PWR.value(1)
        sleep(0.1)
        GSM_PWR.value(0)
        sleep(1.2)
        GSM_PWR.value(1)

def call(number = PHONE_NUMBER):
    if gsm_online_check():
        gsm.disconnect()
    return gsm.atcmd('ATD{};'.format(number))
    

def hangup():
    return gsm.atcmd('ATH')
    

def http_request(method="GET", url=SERVER_URL, headers={}, data=None, json=None):
    try:
        gsm_online_check(True)
        req_status = None
        if DEBUG: print("Sending {} request...".format(method))
        req = requests.request(method=method, url=url, headers=headers, data=data, json=json)
        req_status = [req.status_code, req.reason]
        if req_status is not None:
            print(req_status)
            return req
        else:
            return False
    except Exception as e:
        print("Exception at http_request: ", e)


def get_balance(url=NODE_URL, address=m_address, threshold=100):
    if DEBUG: print("Requesting balance...")
    command = {
      "command": "getBalances",
      "addresses": [address[:81]],
      "threshold": threshold
    }
    #stringified = json.dumps(command) #.encode('utf-8')
    headers = {
        'content-type': 'application/json',
        'X-IOTA-API-Version': '1'
    }
    try:
        response = http_request("POST", url, json=command, headers=headers)
        balance = int(response.json()['balances'][0])
        return balance
    except Exception as e:
        print("Exception at get_balance: ", e)
        return False


# TODO: request address from server
def get_address():
    return True, m_address


def startup_sound():
    buz.value(0)
    sleep_ms(30)
    buz.value(1)
    sleep_ms(200)
    buz.value(0)
    sleep_ms(30)
    buz.value(1)

def end_of_session_sound():
    buz.value(0)
    sleep_ms(200)
    buz.value(1)
    sleep_ms(400)
    buz.value(0)
    sleep_ms(200)
    buz.value(1)
    sleep_ms(400)
    buz.value(0)
    sleep_ms(200)
    buz.value(1)


def hibernate():
    e.set_lut(e.LUT_FULL_UPDATE)
    draw_status(status_def[1])
    rtc.write(2, 1) # write status "sleeping" in RTC
    rtc.write(3, 1) # flag: address in RTC memory
    hst = session_address
    hma = make_qr(session_address)
    for i in range(len(hma)):
        hst += ","
        for j in range(len(hma[i])):
            if hma[i][j]:
                hst += "1"
            else:
                hst += "0"
    rtc.write_string(hst) # write address and QR-Code into RTC memory
    rtc.write(5, 1) # flag: qr-code in RTC memory
    draw_qr(m=hma, scale=3)
    draw_balance(-1)
    draw_rent_time(xs=-1)
    update_display()
    mos.value(0) # turn off 5V AUX
    print("Going into deepsleep...")
    deepsleep()


def r():
    machine.reset()




# RTC memory status registers:
"""
    1: status_old
    2: status
    3: address saved
    5: QR on display

    string: IOTA address
"""




e.set_lut(e.LUT_FULL_UPDATE)
sma = None
status_old = rtc.read(0)
if DEBUG: print("status_old from memory: ", status_old)




# TODO: CHECK WAKE UP REASON
print("\n\nReset cause:",machine.wake_description())
status = 2 # Updating balance




if rtc.read(3):
    if DEBUG: print("Reading session_address from memory...")
    session_address = rtc.read_string().split(',')[0]
else:
    check, s_adr = get_address()
    if check is True:
        session_address = s_adr
if rtc.read(5):
    if DEBUG: print("Reading QR-Code from memory...")
    sst = rtc.read_string().split(',')[1:]
    sma = []
    for i in range(len(sst)):
        sma.append([])
        for j in range(len(sst[i])):
            if sst[i][j] == '1':
                sma[i].append(1)
            else:
                sma[i].append(0)
    if DEBUG: print("QR-Code read.")





session_balance = 2

counter = 0
if BTN1.value() == 0:
    pass
else:
    adc.collect(1, len=10, readmv=True)
    while True:
        if True: #BTN1.value() == 0:
            #break
            LED.value(1)
            startup_sound()
            draw_title()
            draw_status(status_def[status], xs=0)
            draw_balance(session_balance)
            update_display()
            if sma is not None:
                draw_qr(m=sma, scale=3)
            else:
                draw_qr(address=session_address, scale=3)
            update_display()
            e.set_lut(e.LUT_PARTIAL_UPDATE)
            
            if rtc.now()[0] == 1970:  # if RTC is not set up via NTP
                if DEBUG: print("RTC not set up, calling gsm_online_check()")
                gsm_online_check(connect=True)
                print("time()", time())
                sleep(1)
            sleep_ms(1)
            update_old_ticks = 0
            update_new_ticks = 0
            
            while BTN1.value() != 0:
                update_new_ticks = ticks_ms()
                diff = ticks_diff(update_new_ticks, update_old_ticks)
                if diff >= UPDATE_INV or diff < 0:
                    #print("update")
                    update_old_ticks = update_new_ticks
                    
                    if session_balance > 0:
                        if status == 2:
                            status_old = status
                            status = 3
                            print("ss",int(time()))
                            session_start = int(time())
                            print("session_start", session_start)
                    draw_status(status_def[status], xs=0)
                    draw_date()
                    #session_balance = get_balance(url=NODE_URL2, address=m_address_chsum[:81])
                    #session_balance = counter
                    draw_balance(session_balance, ys=100)
                    draw_rent_time()
                    update_display()
                    counter+=1
                print("counter", counter)
                #print("update_old_ticks", update_old_ticks)
                #rint("update_new_ticks", update_new_ticks)
                #print("diff", ticks_diff(update_new_ticks, update_old_ticks))
                print("\n")
                sleep_ms(300)
            break
        print(counter)
        #if gps_location() == (0.0, 0.0):
        #    print("No location fix:", gps_location())
        #else:
        #    print(">>>\nLocation fix:", gps_location())
        sleep(1)
        counter+=1
        #gsm_online_check(True)
        #while True:
        #    
        #    sleep_ms(30)
LED.value(0)