from machine import UART, Pin
from time import sleep, sleep_ms
#import sim800l
import gsm_module

req_server = "https://req.dev.iota.pw"
node_url = "https://nodes.thetangle.org/"
command = {'threshold': 100,
           'command': 'getBalances',
           'addresses': ['SVJQSVYGFUYZHKSQD9OYGSEMCSAWKNXEXMGJSUKQHHDYPDDOTVXYCHFWEAOCZUVOQFANVVLIDAPOTIDY9'
                         ]
            }
headers = {
        'content-type': 'application/json',
        'X-IOTA-API-Version': '1'
    }

GSM_APN  = 'web.vodafone.de' # Your APN
GSM_USER = 'vodafone' # Your User
GSM_PASS = 'vodafone' # Your Pass

# Power on the GSM module
GSM_PWR = Pin(4, Pin.OUT)
GSM_RST = Pin(5, Pin.OUT)
GSM_MODEM_PWR = Pin(23, Pin.OUT)

#tx=27, rx=26
uart = UART(1, baudrate=9600, tx=27, rx=26)
p = gsm_module.SIM800L(uart, GSM_APN, req_server, debug=True)

def gsm_on():
    print("Power up GSM modem...")
    GSM_PWR.value(1)
    sleep(0.1)
    GSM_PWR.value(0)
    GSM_RST.value(1)
    GSM_MODEM_PWR.value(1)
    sleep(1.5)
    GSM_PWR.value(1)

def cmd(command):
    uart.write(command + '\r\n')
    sleep_ms(1000)
    while uart.any() > 0:
        print(uart.readline())

print("ready")
gsm_on()