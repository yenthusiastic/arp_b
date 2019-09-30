'''
  Using your phone:
    - Disable PIN code on the SIM card
    - Check your balance
    - Check that APN, User, Pass are correct and you have internet
  Ensure the SIM card is correctly inserted into the board
  Ensure that GSM antenna is firmly attached

  NOTE: While GSM is connected to the Internet, WiFi can be used only in AP mode

  More docs on GSM module here:
  https://github.com/loboris/MicroPython_ESP32_psRAM_LoBo/wiki/gsm

  Author: Volodymyr Shymanskyy
'''

import machine, time, sys
import gsm
import socket
import urequests as requests
import json
from time import sleep
#import esp32
from machine import RTC
rtc = RTC()

#machine.freq(40000000)

LED = machine.Pin(13, machine.Pin.OUT)
LED.value(1)

wake1 = machine.Pin(15, machine.Pin.IN, machine.Pin.PULL_UP)
#esp32.wake_on_ext0(pin = wake1, level = esp32.WAKEUP_ALL_LOW)

# APN credentials (replace with yours)
GSM_APN  = 'web.vodafone.de' # Your APN
GSM_USER = 'vodafone' # Your User
GSM_PASS = 'vodafone' # Your Pass

# Power on the GSM module
GSM_PWR = machine.Pin(4, machine.Pin.OUT)
GSM_RST = machine.Pin(5, machine.Pin.OUT)
GSM_MODEM_PWR = machine.Pin(23, machine.Pin.OUT)
#GSM_PWR.value(0)
#GSM_RST.value(0)
#GSM_MODEM_PWR.value(0)


def gsm_connect():
    global gsm
    if gsm.status()[0] is 98 : # not started; 0-disconnected 89-IDle
        print("Power up GSM modem...")
        #machine.freq(240000000)
        GSM_PWR.value(1)
        sleep(0.1)
        GSM_PWR.value(0)
        GSM_RST.value(1)
        GSM_MODEM_PWR.value(1)
        sleep(1.5)
        GSM_PWR.value(1)
        # Init PPPoS
        #gsm.debug(True)  # Uncomment this to see more logs, investigate issues, etc.
    if gsm.status()[0] is 98 or 0:
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
        #machine.freq(40000000)


def gsm_online_check():
    if not gsm.status()[0] == 1:
        gsm_connect()


def gsm_shutdown():
    if gsm.stop():
        GSM_PWR.value(1)
        sleep(0.1)
        GSM_PWR.value(0)
        sleep(1.2)
        GSM_PWR.value(1)

# GSM connection is complete.
# You can now use modules like urequests, uPing, etc.
# Let's try socket API:
"""
import socket
addr_info = socket.getaddrinfo("iota.pw", 80)
addr = addr_info[0][-1]
s = socket.socket()
s.connect(addr)

while True:
    data = s.recv(500)
    print(str(data, 'utf8'), end='')
"""
# You should see terminal version of StarWars episode
# Just like this: https://asciinema.org/a/1457

address = "SVJQSVYGFUYZHKSQD9OYGSEMCSAWKNXEXMGJSUKQHHDYPDDOTVXYCHFWEAOCZUVOQFANVVLIDAPOTIDY9"
node_url = "https://nodes.thetangle.org/"
#command = {'threshold': 100, 'command': 'getBalances', 'addresses': ['SVJQSVYGFUYZHKSQD9OYGSEMCSAWKNXEXMGJSUKQHHDYPDDOTVXYCHFWEAOCZUVOQFANVVLIDAPOTIDY9']}




def http_get(url, port=80):
    gsm_online_check()
    print("Sending get request...")
    _, _, host, path = url.split('/', 3)
    addr = socket.getaddrinfo(host, port)[0][-1]
    s = socket.socket()
    s.connect(addr)
    s.send(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, host), 'utf8'))
    while True:
        data = s.recv(100)
        if data:
            print(str(data, 'utf8'), end='')
        else:
            break
    s.close()


def send_request(url="https://req.dev.iota.pw/"):
    try:
        gsm_online_check()
        req_status = None
        print("sending request...")
        json_data = [{"hardwareID": 1}, {"vbat": 3850}]
        #req = requests.get(url)
        req = requests.post(url, json=json_data)
        req_status = [req.status_code, req.reason]
        if req_status is not None:
            pass
        else:
            return False
        print(req_status)
    except Exception as e:
        print("Exception at request: ", e)


def get_balance(url=node_url, address=address, threshold=100):
    gsm_online_check()
    print("Requesting balance...")
    command = {
      "command": "getBalances",
      "addresses": [
        address
      ],
      "threshold": threshold
    }
    #stringified = json.dumps(command) #.encode('utf-8')
    headers = {
        'content-type': 'application/json',
        'X-IOTA-API-Version': '1'
    }
    response = requests.get(url, json=command, headers=headers)
    return response

"""
gsm_connect()
LED.value(0)
sleep(0.2)
LED.value(1)
sleep(0.2)
LED.value(0)
sleep(0.2)
LED.value(1)
sleep(0.2)
LED.value(0)
sleep(0.2)
LED.value(1)

http_get("https://req.dev.iota.pw/")
print("\n*** DEEPSLEEP ***")
LED.value(0)
#machine.deepsleep()
"""
