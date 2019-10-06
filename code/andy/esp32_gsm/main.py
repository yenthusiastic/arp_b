'''
  Based on:
  https://github.com/loboris/MicroPython_ESP32_psRAM_LoBo/wiki/gsm
'''


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

m_address = "SVJQSVYGFUYZHKSQD9OYGSEMCSAWKNXEXMGJSUKQHHDYPDDOTVXYCHFWEAOCZUVOQFANVVLIDAPOTIDY9"
m_status = None
m_states = {"offline": 0, "parked":1, "rented":2, "broken":3, "stolen":4}


import machine, time, sys
import gsm
import socket
import urequests as requests
import json
from time import sleep
from machine import RTC
rtc = RTC()


# Setup GSM Module Pins
GSM_PWR = machine.Pin(4, machine.Pin.OUT)
GSM_RST = machine.Pin(5, machine.Pin.OUT)
GSM_MODEM_PWR = machine.Pin(23, machine.Pin.OUT)
#GSM_PWR.value(0)
#GSM_RST.value(0)
#GSM_MODEM_PWR.value(0)

# Setup User IO Pins
LED = machine.Pin(13, machine.Pin.OUT)
LED.value(1)
BTN1 = machine.Pin(15, machine.Pin.IN, machine.Pin.PULL_UP)


def gsm_connect():
    global gsm
    if gsm.status()[0] is 98 : # 98-not started; 89-idle; 0-disconnected
        print("Power up GSM modem...")
        #machine.freq(240000000)
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
        for retry in range(8):
            if gsm.atcmd('AT'):
                break
            else:
                sys.stdout.write('.')
                time.sleep_ms(3000)
        else:
            raise Exception("Modem not responding!")
        print()
        print("Connecting to GSM...")
        gsm.connect()
        while gsm.status()[0] != 1:
            pass
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
        print("Sending http_get request...")
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
      "addresses": [address],
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

"""
while True:
    if BTN1.value() == 0:
        break
    gsm_online_check()
"""