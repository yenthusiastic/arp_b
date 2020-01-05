'''
  MicroPython fork by loboris:
  https://github.com/loboris/MicroPython_ESP32_psRAM_LoBo/
'''

# ===== IMPORTS ========
from sys import stdout 
from machine import Pin, SPI, ADC, UART, I2C, GPS, RTC, deepsleep, reset, wake_description, wake_reason
import gsm
import socket
import urequests as requests
import json
from time import sleep, sleep_ms, ticks_ms, ticks_diff, time, strftime
#import epaper2in9
#import framebuf
# ===== /IMPORTS ========


# ===== CONFIG ========

# APN Credentials
GSM_APN  = 'web.vodafone.de'
GSM_USER = 'vodafone'
GSM_PASS = 'vodafone'

# Module Settings
HARDWARE_ID = const(55)
API_KEY = "2ed617ed018c0b13f209fc0bbe75ab8ab1a1d303"
PHONE_NUMBER = '+491745851814'
SERVER_URL = "https://req.dev.iota.pw/"
BACKEND_URL = "https://be.dev.iota.pw"
NODE_URL2 = "https://nodes.iotadev.org/"
NODE_URL = "https://nodes.thetangle.org/"

UPDATE_INV = const(1000)

RENT_TIME_FACTOR = 0.5

# Accelerometer Config
ACC_ADDRESS = const(0x18)
ACC_INTERRUPT_PIN = 14
# Registers
REG_WHOAMI                = const(0x0F)   # Who am I (0x33)
REG_TEMPCFG               = const(0x1F)
REG_ACC_CONFIG            = const(0x20)   # Axis configurations and power-modes
REG_HIGH_PASS_FILTER      = const(0x21)   # Configuring the high-pass filters
REG_INT_CONFIG            = const(0x22)   # Interrupt configurations
REG_SCALE_MODES           = const(0x23)   # Set-up the full-scale of the accelerometer
REG_LATCH_CONFIG          = const(0x24)   # Latch configurations
REG_INT_LOGICS            = const(0x30)   # Interrupt configurations (different axis)
REG_INTERRUPT             = const(0x31)   # Interrupt status
REG_THRESHOLD             = const(0x32)   # Acceleration threshold
REG_DURATION              = const(0x33)   # Acceleration duration


#m_address = "SVJQSVYGFUYZHKSQD9OYGSEMCSAWKNXEXMGJSUKQHHDYPDDOTVXYCHFWEAOCZUVOQFANVVLIDAPOTIDY9UCQYMMMXX"
#dev1
# 0:
# m_address = "CFQFHKJSEJEO9DMNGDCFBROYQIW9WYGSNLYZSIQQQPMUHTEPZGYDOWGLFOWPZKOYFFXSZXEMRECVYHMOZTBULVLBMW"
# 1:
m_address = "9REDAGQZMSRGWMVXNYEAS9ILNWNZFGATYKKHTGXWVUWGPCECWYCD9ZIVZGMZYHYTWVBNJO9I99QXYSYYWNQHQDKMBB"
m_states = {"offline": 0, "sleeping":1, "parked":2, "rented":3, "broken":4, "stolen":5}

DEBUG = True
DEMO = True
# ===== /CONFIG ========


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


status = 0
status_old = 0
qr_display = 0
session_address = ""
session_balance = 0
session_start = 0
session_rent_time = 0



# Create RTC
rtc = RTC()

# Setup GSM Module Pins
GSM_PWR = Pin(4, Pin.OUT)
GSM_RST = Pin(5, Pin.OUT)
GSM_MODEM_PWR = Pin(23, Pin.OUT)
#GSM_PWR.value(0)
#GSM_RST.value(0)
#GSM_MODEM_PWR.value(0)

# Setup User IO Pins
btn1 = Pin(0, Pin.IN, Pin.PULL_UP)
led = Pin(13, Pin.OUT, value=0)


# Accelerometer Interrupt wake-up pin
acc_int = Pin(14, Pin.IN, Pin.PULL_DOWN)

# wake-up source for deepsleep
#rtc.wake_on_ext0(pin=btn1, level=0) #wakeup at btn low
rtc.wake_on_ext0(pin=acc_int, level=1) # wakeup at acc_int high

# MOSFET for 5V AUX
mos = Pin(12, Pin.OUT, value=0)

# Alarm Buzzer
buz = Pin(2, Pin.OUT, value=1)
buz.value(0)
sleep_ms(50)
buz.value(1)



# CO2 sensor, MH-Z14
adc=ADC(Pin(36))

# Battery sense Pin
bat = ADC(Pin(39))
bat.atten(ADC.ATTN_11DB) # 0 - 3.6 V

# GPS
# RX is not used
gps = GPS(UART(2, rx=35, tx=33, baudrate=9600, bits=8, parity=None, stop=1, timeout=1500, buffer_size=1024, lineend='\r\n'))
gps.startservice()


# PM sensor, SDS011
PM10_PIN = Pin(19, Pin.IN)
PM25_PIN = Pin(18, Pin.IN)

# Turn on auxiliary sensors
mos.value(1)




import lis3dh_git as lis3dh
import bme280_float
#import sds011 # using PWM output

# I2C
i2c = I2C(0, I2C.MASTER, scl=Pin(22), sda=Pin(21), freq=400000)

acc = lis3dh.LIS3DH_I2C(i2c)
acc.data_rate = lis3dh.DATARATE_100_HZ
acc.range = lis3dh.RANGE_4_G


# temperature/ atmosperic pressure/ humidity, BME280
bme = bme280_float.BME280(i2c=i2c)


# ===== DISPLAY ========
import epaper2in9
import framebuf

spi = SPI(2, baudrate=2000000, polarity=1, phase=0, sck=Pin(25), mosi=Pin(15), miso=Pin(0))
btn1 = Pin(0, Pin.IN, Pin.PULL_UP)

dc=Pin(32)
rst=Pin(14)
busy=Pin(34)
cs=Pin(33)

BLACK = const(0)
WHITE = const(1)

W = const(128)
H = const(296)

buf = bytearray(W * H // 8)
fb = framebuf.FrameBuffer(buf, W, H, framebuf.MONO_HLSB)
fb.fill(WHITE)

e=epaper2in9.EPD(spi, cs, dc, rst, busy)
e.init()

def draw_title():
    fb.fill_rect(0,0,W,10, BLACK)
    fb.text("B I K O T A", 20, 3, WHITE)
    #e.draw_filled_rectangle(buf, 0,10,127,11, True)
    #e.draw_filled_rectangle(bufy, 0,15,127,168, True)
    fb.fill_rect(0,10,W,3, BLACK)
    fb.fill_rect(0,35,W,3, BLACK)

def draw_status(stat="Undefined", xs=0, ys=20):
    fb.fill_rect(0, ys-6, W, 21, WHITE)
    if xs >= 0:
        if xs == 0:
            xs = int((W - (len(stat) * 8)) / 2) 
        fb.text(str(stat), xs, ys, BLACK)

def draw_date(xs=0, ys=45):
    if rtc.now()[0] != 1970:
        fb.fill_rect(0, ys, xs+64, 11, WHITE)
        if xs>=0:
            dt=rtc.now()[:6]
            fb.text("{}.{}.{}".format(dt[2], dt[1], dt[0]-2000), 0, ys, BLACK)


def draw_balance(iota=session_balance, xs=0, ys=100):
    fb.fill_rect(0, ys, W, 8, WHITE)
    if iota >= 0:
        fb.text("Balance: {}i".format(iota), 0, ys, BLACK)
    #fb.fill_rect(0,ys+8,127,11, 1)
    #fb.text("{} i".format(iota),0,  ys+10, 0)

def draw_rent_time(xs=0, ys=120):
    global status, status_old, session_rent_time, session_balance, session_start, parking_old_ticks
    status = status
    status_old = status_old
    session_rent_time= session_rent_time
    session_balance = session_balance
    session_start = session_start
    fb.fill_rect(0, ys, W, 8, WHITE)
    if xs >= 0:
        if session_start > 0:
            session_rent_time = session_balance * RENT_TIME_FACTOR * 60
            delta = int(time()) - session_start
            if delta > session_rent_time and status == 3:
                status_old = status
                status = 4
                parking_old_ticks = ticks_ms()
                end_of_session_sound()
            if status == 3:
                s_delta = session_rent_time - delta
                dmin = int(s_delta // 60)
                dsec = int(s_delta % 60)
                # TODO: add zero padding
                fb.text("Session: {}:{}".format(dmin, dsec), 0, ys, BLACK)
            elif status == 4:
                draw_balance(iota = -1)
                fb.text("Park the bike!", 0, ys, BLACK)
                

def update_display():
    e.set_frame_memory(buf, 0, 0, W, H)
    e.display_frame()


def clear_buf(color = WHITE):
    fb.fill_rect(0, 0, W, H, color)


def draw_qr(m=None, address=None, xs=2, ys=170, scale=1):
    if DEBUG: print("draw_qr")
    fb.fill_rect(xs, ys, W, H-ys, WHITE)   # clear QR area with WHITE fill
    if m == None:
        if DEBUG: print("No QR code provided, creating QR code.")
        if address == None:
            address = m_address_chsum
        m = make_qr(address)
    if DEBUG: print("Drawing QR code.")
    # TODO: fix watchdog trigger from code below
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
    if DEBUG: print("Creating QR code...")
    from uQR import QRCode
    if DEBUG: print("Imported QR library.")
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


def acc_set_interrupt():
    global acc
    if DEBUG: print("Writing accelerometer registers...")
    acc._i2c.writeto_mem(ACC_ADDRESS, REG_HIGH_PASS_FILTER, b'\x09')
    acc._i2c.writeto_mem(ACC_ADDRESS, REG_INT_CONFIG, b'\x40')
    acc._i2c.writeto_mem(ACC_ADDRESS, REG_SCALE_MODES, b'\x00')
    acc._i2c.writeto_mem(ACC_ADDRESS, REG_LATCH_CONFIG, b'\x00')
    acc._i2c.writeto_mem(ACC_ADDRESS, REG_THRESHOLD, b'\x0A') # x06
    acc._i2c.writeto_mem(ACC_ADDRESS, REG_DURATION, b'\x03')  # x00
    acc._i2c.writeto_mem(ACC_ADDRESS, REG_INT_LOGICS, b'\x2A')
    acc._i2c.writeto_mem(ACC_ADDRESS, REG_ACC_CONFIG, b'\x5F')
    if DEBUG: print("Accelerometer registers written.")


#========== SENSORS =================
def get_bat_voltage():
    volt = (bat.read() / 4095) * 3.99  # raw Voltage
    #return volt * 1.99                 # voltage divider
    return float("{0:.2f}".format(volt * 1.99))
    

"""
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
    return
"""

def get_pm(p10=PM10_PIN, p25=PM25_PIN):
    while p10.value() == 0:
        pass
    st_10=ticks_ms()
    while p10.value() == 1:
        pass
    sp_10=ticks_ms()
    while p25.value() == 0:
        pass
    st_25=ticks_ms()
    while p25.value() == 1:
        pass
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
    print('Failed to read BME sensor: ', e)
    return None


def gps_location():
    data = gps.getdata()
    if gps.getdata()[0][0] != 1900:
        return (data[1], data[2])
    else:
        return False
#========== /SENSORS =================



#========== GSM =================
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
        if DEBUG: stdout.write('Waiting for AT command response...')
        for retry in range(50):
            if gsm.atcmd('AT'):
                break
            else:
                if DEBUG: stdout.write('.')
                sleep_ms(500)
        else:
            raise Exception("Modem not responding!")
        if DEBUG: print()
        if DEBUG: print("Connecting to GSM...")
        gsm.connect()
        while gsm.status()[0] != 1:
            stdout.write('.')
            sleep_ms(200)
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
    if DEBUG: print("Shuting down GSM module...")
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

#========== /GSM =================


#========== HTTP =================
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
def get_address(online=True):
    if online:
        try:
            if DEBUG: print("Requesting new address...")
            r = http_request(method="GET", url=BACKEND_URL + "/address/" + str(HARDWARE_ID))
            if DEBUG: print("Got: ", r.text)
            adr = json.loads(r.text)["Session address"]
            if adr is not None:
                return True, adr
            else:
                return False, None
        except Exception as e:
            print("Exception at get_address: ", e)
            return False, None
    else:
        return True, m_address
#========== /HTTP =================


#========== SOUND =================
def sound(on_t, off_t, reps):
    for i in range(reps):
        buz.value(0)
        sleep_ms(on_t)
        buz.value(1)
        sleep_ms(off_t)

def buz_beeb():
    sound(50, 0, 1)

def startup_sound():
    sound(20,100,2)

def start_of_session_sound():
    sound(30,200,3)

def end_of_session_sound():
    sound(200,400,3)
    
def alarm_sound():
    sound(500,500,3)
#========== /SOUND =================


# TODO: fix watchdog reset at draw_qr
def hibernate():
    if DEBUG: print("Preparing for hibernation...")
    acc_set_interrupt()
    mos.value(0) # turn off 5V AUX
    e.set_lut(e.LUT_FULL_UPDATE)
    draw_title()
    draw_status(status_def[1])
    check, hst = get_address()
    """
    for i in range(2):
        check, s_adr = get_address()
        print("get_address: {0}, {1}".format(check, s_adr))
        if check is True:
            session_address = s_adr
            break
        else:
            print("get_address: False, try again...")
    """
    gsm_shutdown()
    hma = make_qr(hst)
    rtc.write(2, 1) # write status "sleeping" in RTC
    rtc.write(3, 1) # flag: address in RTC memory
    
    if DEBUG: print("Making RTC string.")
    for i in range(len(hma)):
        hst += ","
        for j in range(len(hma[i])):
            if hma[i][j]:
                hst += "1"
            else:
                hst += "0"
    if DEBUG: print("Writing QR and address to RTC memory...")
    rtc.write_string(hst) # write address and QR-Code into RTC memory
    rtc.write(5, 1) # flag: qr-code in RTC memory
    if DEBUG: print("Draw 'sleep' frame.")
    draw_balance(-1)
    draw_rent_time(xs=-1)
    draw_qr(m=hma, scale=3)
    update_display()
    print("Going into deepsleep...")
    deepsleep()


def r():
    reset()




# RTC memory status registers:
"""
    1: status_old
    2: status
    3: address saved
    5: QR on display

    string: IOTA address
"""


# TODO: CHECK WAKE UP REASON
# if not hibernate wakeup, just set up everything
# if hibernate wakeup(3) read stuff from rtc memory

print("\n\nReset cause:",wake_description())
status = 2 # Updating balance
# 'Deepsleep wake-up'
# reason (3, 1)


#========== INIT =================
if btn1.value() is not 0:
    if wake_reason()[0] != 3:
        hibernate()
    else:  # wake-up from hibernation
        e.set_lut(e.LUT_FULL_UPDATE)
        session_matrix = None
        status_old = rtc.read(0)
        if DEBUG: print("status_old from memory: ", status_old)

        if rtc.read(3):
            if DEBUG: print("Reading session_address from memory...")
            session_address = rtc.read_string().split(',')[0]
            if DEBUG and session_address is not None: print("session_address read.")
        else:
            print("No address in RTC memory!")
            print("Wakeup reason: ", wake_reason()[0])
            """
            for i in range(2):
                check, s_adr = get_address()
                print("get_address: {0}, {1}".format(check, s_adr))
                if check is True:
                    session_address = s_adr
                    break
                else:
                    print("get_address: False, try again...")
            """
            """
            check, s_adr = get_address()
            print("get_address: {0}, {1}".format(check, s_adr))
            if check is True:
                session_address = s_adr
                
            else:
                print("get_address: False, reseting")
                r()
            """
            
        if rtc.read(5):
            if DEBUG: print("Reading QR-Code from memory...")
            sst = rtc.read_string().split(',')[1:]
            session_matrix = []
            for i in range(len(sst)):
                session_matrix.append([])
                for j in range(len(sst[i])):
                    if sst[i][j] == '1':
                        session_matrix[i].append(1)
                    else:
                        session_matrix[i].append(0)
            if DEBUG: print("QR-Code read.")
#========== /INIT =================


#========== MAIN =================
print("HardwareID: ", HARDWARE_ID)
print("Battery Voltage: ",get_bat_voltage())

session_balance = 0
timestamp = strftime("%Y-%m-%d %H:%M:%S")


jsn= {"hardwareID":"1","address":"Postman_test","latitude":"61.123","longitude":"7.933","temperature":"5.0","humidity":"30.5", "timestamp":timestamp}
#r2=http_request(method="POST", url="https://be.dev.iota.pw/data", json=jsn)


counter = 0
demo_balance = 0

if btn1.value() == 0:
    pass
else:
    adc.collect(1, len=10, readmv=True)
    while True:
                
        if btn1.value() is not 0:
            led.value(1)
            startup_sound()
            draw_title()
            draw_status(status_def[status], xs=0)
            draw_balance(session_balance)
            update_display()
            if session_matrix is not None:
                draw_qr(m=session_matrix, scale=3)
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
            
            new_ticks = ticks_ms()
            update_old_ticks = 0
            balance_old_ticks = new_ticks
            parking_old_ticks = new_ticks
            
            
            while btn1.value() != 0:
                new_ticks = ticks_ms()
                update_diff = ticks_diff(new_ticks, update_old_ticks)
                balance_diff = ticks_diff(new_ticks, balance_old_ticks)
                parking_diff = ticks_diff(new_ticks, parking_old_ticks)
                
                if update_diff >= UPDATE_INV or update_diff < 0:
                    #print("update")
                    update_old_ticks = new_ticks
                    
                    # Start session
                    if session_balance > 0:
                        if status == 2:
                            status_old = status
                            status = 3 # Session running
                            start_of_session_sound()
                            session_start = int(time())
                            if DEBUG: print("session_start", session_start)
                            
                    draw_date()
                    draw_balance(session_balance, ys=100)
                    draw_rent_time()
                    draw_status(status_def[status], xs=0)
                    update_display()
                    counter+=1
                    
                # UPDATING BALANCE
                if status == 2:
                    session_balance = get_balance(url=NODE_URL2, address=session_address[:81])
                    #session_balance = counter
                    if DEMO:
                        if btn1.value() == 0:
                            demo_balance = 1
                            session_balance = demo_balance
                            print("DEMO MODE ACTIVATED\nsession_balance = 1\nRelease button...")
                            sleep(2)
                    
                #SESSION RUNNING
                # TODO: ensure balance update happens only x seconds into the running session
                elif status == 3:
                    if balance_diff > 80000: # check balance every 80 seconds
                        balance_old_ticks = new_ticks
                        session_balance = get_balance(url=NODE_URL2, address=session_address[:81])
                        if DEMO:
                            if demo_balance > 0:
                                session_balance = demo_balance
                # SESSION OVER
                if status == 4:
                    if parking_diff > 10:
                        # TODO: check for no vibration = bike is parked
                        if True:
                            hibernate()
                
                print("counter", counter)
                #print("update_old_ticks", update_old_ticks)
                #rint("new_ticks", new_ticks)
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
led.value(0)
#========== /MAIN =================