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
from machine import Pin, UART, I2C, GPS, DHT, RTC, deepsleep
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

# RX is not used
gps = GPS(UART(2, rx=35, tx=33, baudrate=9600, bits=8, parity=None, stop=1, timeout=1500, buffer_size=1024, lineend='\r\n'))


#pm = sds011.SDS011(UART(1, baudrate=9600, tx=12, rx=34))

dht = DHT(Pin(2), DHT.DHT2X)

#pm.sleep()
#gps.startservice()

PM10_PIN = Pin(19, Pin.IN)
PM25_PIN = Pin(18, Pin.IN)

#i2c = I2C(scl=Pin(22), sda=Pin(21))
i2c = I2C(0, I2C.MASTER, scl=Pin(22), sda=Pin(21), freq=400000)
import mpu6050 as mpu
mpu.init_sensor(i2c)


# =====TEMPORARY DISPLAY========

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
    for y in range(len(m)*2):                   # Scaling the bitmap by 2
        for x in range(len(m[0])*2):            # because my screen is tiny.
            value = m[y//2][x//2]   # Inverting the values because
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


def get_dht():
    res, tmp, hum = dht.read()
    if res:
        return (tmp, hum)
    else:
        return False
    

def gps_location():
    data = gps.getdata()
    return (data[1], data[2])


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
    d.font(d.FONT_DejaVu24)
    d.text(d.CENTER, 45, "SLEEPING", d.YELLOW)
    deepsleep()

print("\n\n",machine.wake_description())
#if machine.reset_cause() == machine.DEEPSLEEP_RESET:
#        print('reset_cause: deepsleep')
#else:
#    print("reset_cause:", machine.reset_cause())


#"""

counter = 0
if BTN1.value() == 0:
    pass
else:
    while True:
        if True: #BTN1.value() == 0:
            #break
            make_qr(address=adr)
            d.text(d.CENTER, 50, "Balance: 0 i", d.WHITE)
            while BTN1.value() != 0:
                balance = get_balance(address=adr[:81])
                d.text(d.CENTER, 50, "Balance: xxxxxxxxx i", d.BLACK)
                d.text(d.CENTER, 50, "Balance: {} i".format(balance), d.WHITE)
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
    d.text(d.CENTER, 50, "   !!! TERMINATED !!!   ", d.RED)
