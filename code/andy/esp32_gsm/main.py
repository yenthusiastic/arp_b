'''
  Based on:
  https://github.com/loboris/MicroPython_ESP32_psRAM_LoBo/wiki/gsm
'''

# =====CONFIG========

# APN Credentials
GSM_APN  = 'web.vodafone.de'
GSM_USER = 'vodafone'
GSM_PASS = 'vodafone'

# Module Settings
HARDWARE_ID = 1
API_KEY = "2ed617ed018c0b13f209fc0bbe75ab8ab1a1d303"
PHONE_NUMBER = '+491745851814'
SERVER_URL = "https://req.dev.iota.pw/"
NODE_URL = "https://nodes.thetangle.org/"

# dev-strings
json_data = [{"hardwareID": 1}, {"vbat": 3850}]

adr="LVYDWAFMEZRAQKPYOXYBJZXDKJCHGFTPPEQN9LIODWOMPVYJ9WRRNOBL9STKHUINQJZQ9RTZFQKEQWYHABJBATFLVX"
adr2="LMXVMOYJRWECKHVPADXIBYZDW9HETZQVPJIJSZQPWBHIYGALPUAGKIVETNYJVEWFD9AQKGPTTAGWUYPLZBFBTXVBFX"
m_address = "SVJQSVYGFUYZHKSQD9OYGSEMCSAWKNXEXMGJSUKQHHDYPDDOTVXYCHFWEAOCZUVOQFANVVLIDAPOTIDY9"
m_address_chsum = "SVJQSVYGFUYZHKSQD9OYGSEMCSAWKNXEXMGJSUKQHHDYPDDOTVXYCHFWEAOCZUVOQFANVVLIDAPOTIDY9UCQYMMMXX"
m_status = None
m_states = {"offline": 0, "parked":1, "rented":2, "broken":3, "stolen":4}

# ===================


import machine, sys 
from machine import Pin, ADC, UART, I2C, GPS, DHT, RTC, deepsleep
import gsm
import sds011
import socket
import urequests as requests
import json
from time import sleep
from time import sleep_ms
from time import ticks_ms
rtc = RTC()

"""
Pins used
LED: 13 (build in)
PM: 12, 14
BTN: 15
GSM: 4, 5, 23, 26, 27
DHT22: 25


"""

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

rtc.wake_on_ext0(pin=BTN1, level=0)

adc=ADC(Pin(36))

# RX is not used
gps = GPS(UART(2, rx=35, tx=33, baudrate=9600, bits=8, parity=None, stop=1, timeout=1500, buffer_size=1024, lineend='\r\n'))
gps.startservice()


#pm = sds011.SDS011(UART(1, baudrate=9600, tx=12, rx=34))
#pm.sleep()
PM10_PIN = Pin(19, Pin.IN)
PM25_PIN = Pin(18, Pin.IN)

dht = DHT(Pin(2), DHT.DHT2X)

#i2c = I2C(scl=Pin(22), sda=Pin(21))
i2c = I2C(0, I2C.MASTER, scl=Pin(22), sda=Pin(21), freq=400000)
import mpu6050 as mpu
mpu.init_sensor(i2c)

LED = Pin(13, Pin.OUT)
LED.value(0)

def r():
    machine.reset()


# =====TEMPORARY DISPLAY========
from machine import Pin, SPI
#import epaper2in9b_mod as epaper2in9b
import epaper2in9
spi = SPI(2, baudrate=2000000, polarity=1, phase=0, sck=Pin(25), mosi=Pin(15), miso=Pin(0))

dc=Pin(32)
rst=Pin(12)
busy=Pin(34)
cs=Pin(33)

black = 0
white = 1

w = 128
h = 296
x = 0
y = 0

import framebuf
buf = bytearray(128 * 296 // 8)
fb = framebuf.FrameBuffer(buf, 128, 296, framebuf.MONO_HLSB)
#bufy = bytearray(128 * 296 // 8)
#fby = framebuf.FrameBuffer(bufy, 128, 296, framebuf.MONO_HLSB)
#fby.fill(white)
fb.fill(white)
#fb.text('Hello World',30,0,black)

#e.display_frame(buf,bufy)
e=epaper2in9.EPD(spi, cs, dc, rst, busy)
e.init()

"""
128x160 RGB TFT Touch Display with ST7735 Controller
import display
d = display.TFT()
d.init(d.ST7735B, mosi=12, miso=34, clk=25, cs=33, dc=32, width=130, height=161, speed=10000000, splash=False)
d.set_bg(d.BLACK)
d.clear()
d.font(d.FONT_Tooney)
d.text(d.CENTER, 0, "BikOTA", d.GREEN, transparent=False)
d.font(d.FONT_DefaultSmall)
d.text(2, 32, "ID: {}".format(machine.nvs_getint('hardwareID')), d.WHITE)

def draw_qr(m, xs=20, ys=71):
    for y in range(len(m)*2):                   
        for x in range(len(m[0])*2):            
            value = m[y//2][x//2]   
            if value == 0:
                value=0xFFFFFF
            else:
                value=0x000000
            d.pixel(xs+x, ys+y, value)

def make_qr(address=m_address):
    d.font(d.FONT_DefaultSmall)
    d.text(d.CENTER, 80, "Generating Address...", d.WHITE)
    from uQR import QRCode
    qr=QRCode(border=2)
    qr.clear()
    qr.add_data(address)
    m_address_matrix = qr.get_matrix()
    d.text(d.CENTER, 80, "Generating Address...", d.BLACK)
    draw_qr(m_address_matrix)
"""

def make_qr(address=m_address):
    print("Making QR code...")
    from uQR import QRCode
    qr=QRCode(border=0)
    #qr.clear()
    qr.add_data(address)
    m_address_matrix = qr.get_matrix()
    return m_address_matrix

def draw_qr(m=None, address=None, xs=0, ys=166, scale=1):
    if m == None:
        if address == None:
            address = m_address
        m = make_qr(address) 
    for y in range(len(m)*scale):
        for x in range(len(m[0])*scale):
            value = m[y//scale][x//scale]
            if value == 0:
                value=0xFF
            else:
                value=0x00
            fb.pixel(xs+x, ys+y, value)

def draw_title():
    fb.text("B I K O T A", 20, 1, 0)
    #e.draw_filled_rectangle(buf, 0,10,127,11, True)
    #e.draw_filled_rectangle(bufy, 0,15,127,168, True)
    fb.fill_rect(0,10,127,3, black)
    fb.fill_rect(0,25,127,3, black)

def draw_status(stat="SLEEPING"):
    fb.fill_rect(0,14,127,11, 1)
    fb.text(str(stat), 30, 15, 0)

def draw_balance(iota=100):
    fb.text("Balance:".format(iota), 0, 45, 0)
    fb.fill_rect(0,53,127,11, 1)
    fb.text("{} i".format(iota),0,  55, 0)
    

def update_display():
    #e.display_frame(buf,bufy)
    e.set_frame_memory(buf, x, y, w, h)
    e.display_frame()
#===============================




def checkms(t):
    while t.value()==0:
        start=ticks_ms()
    while t.value()==1:
        stop=ticks_ms()
    print("Pulse:", (stop-start)-2)


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
    print("PM10:", (sp_10-st_10)-2)
    print("PM25:", (sp_25-st_25)-2)



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



def get_dht():
    res, tmp, hum = dht.read()
    if res:
        return (tmp, hum)
    else:
        return False
    

def gps_location():
    data = gps.getdata()
    if gps.getdata()[0][0] != 1900:
        return (data[1], data[2])
    else:
        return False


def gsm_connect():
    global gsm
    if gsm.status()[0] is 98 : # 98-not started; 89-idle; 0-disconnected
        print("Power up GSM modem...")
        #freq(240000000)
        GSM_PWR.value(1)
        sleep(0.1)
        GSM_PWR.value(0)
        GSM_RST.value(1)
        GSM_MODEM_PWR.value(1)
        sleep(1.5)
        GSM_PWR.value(1)
        #gsm.debug(True)
    if gsm.status()[0] is 98 or 89 or 0:
        gsm.start(tx=27, rx=26, apn=GSM_APN, user=GSM_USER, password=GSM_PASS)
        sys.stdout.write('Waiting for AT command response...')
        for retry in range(50):
            if gsm.atcmd('AT'):
                break
            else:
                sys.stdout.write('.')
                sleep_ms(500)
        else:
            raise Exception("Modem not responding!")
        print()
        print("Connecting to GSM...")
        gsm.connect()
        while gsm.status()[0] != 1:
            sys.stdout.write('.')
            sleep_ms(10)
            #pass
        print('IP:', gsm.ifconfig()[0])
        if rtc.now()[0] == 1970:
            print("Update RTC from NTP server...")
            rtc.ntp_sync(server="hr.pool.ntp.org", tz="CET-1CEST")
            print("RTC updated.")


def gsm_online_check(connect=False):
    if gsm.status()[0] == 1:
        return True
    else:
        if connect:
            gsm_connect()
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
        print("Sending {} request...".format(method))
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
    print("Requesting balance...")
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
        response = http_request("GET", url, json=command, headers=headers)
        balance = int(response.json()['balances'][0])
        return balance
    except Exception as e:
        print("Exception at get_balance: ", e)
        return False


def hibernate():
    #d.font(d.FONT_DejaVu24)
    #d.text(d.CENTER, 45, "SLEEPING", d.YELLOW)
    deepsleep()

print("\n\n",machine.wake_description())
#if machine.reset_cause() == machine.DEEPSLEEP_RESET:
#        print('reset_cause: deepsleep')
#else:
#    print("reset_cause:", machine.reset_cause())


#"""


def draw_status_updating():
    draw_status("Updating")
    update_display()
    sleep(0.5)
    draw_status("Updating.")
    update_display()
    sleep(0.5)
    draw_status("Updating..")
    update_display()
    sleep(0.5)
    draw_status("Updating...")
    update_display()
    sleep(0.5)

def draw_qr_updating():
    fb.fill_rect(0,166,127,296, white)
    draw_qr(m=m_qr, scale=1)
    update_display()
    #sleep(0.5)
    fb.fill_rect(0,166,127,296, white)
    draw_qr(m=m_qr, scale=2)
    update_display()
    #sleep(0.5)
    fb.fill_rect(0,166,127,296, white)
    draw_qr(m=m_qr, scale=3)
    update_display()
    #sleep(0.5)


counter = 0
if BTN1.value() == 0:
    pass
else:
    while True:
        if True: #BTN1.value() == 0:
            #break
            LED.value(1)
            draw_qr(address=adr, scale=3)
            draw_title()
            draw_status()
            draw_balance()
            update_display()
            #d.text(d.CENTER, 50, "Balance: 0 i", d.WHITE)
            while BTN1.value() != 0:
                e.set_lut(e.LUT_PARTIAL_UPDATE)
                draw_status("Checking Balance")
                balance = get_balance(address=adr[:81])
                draw_balance(balance)
                update_display()
            #    d.text(d.CENTER, 50, "Balance: xxxxxxxxx i", d.BLACK)
            #    d.text(d.CENTER, 50, "Balance: {} i".format(balance), d.WHITE)
                #sleep(5)
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
    #"""
    #d.text(d.CENTER, 50, "   !!! TERMINATED !!!   ", d.RED)
LED.value(0)