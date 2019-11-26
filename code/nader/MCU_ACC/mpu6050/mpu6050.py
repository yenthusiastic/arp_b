# Registers
ACC_CONFIG            = const(0x1C)   # Configures the Digital High Pass Filter as well as the full scale of the acceleration sensor 
MOTION_THRESHOLD      = const(0x1F)   # Sets the desired treshold of the motion (1LSB = 2mG)
MOTION_DURATION       = const(0x20)   # Sets the desired duration of the motion in ms 
INT_STATUS            = const(0x3A)   # Shows the interrupt status of each interrupt generation source
I2C_BYPASS_ENABLE     = const(0x37)   # Configures the behaviour of the interrupt signal at the INT pins
INT_ENABLE            = const(0x38)   # Enables the interrupt generation by interrupt sources
POWER_MGMT_1          = const(0x6B)   # Configures the power mode and clock source as well as resetting
POWER_MGMT_2          = const(0x6C)   # Configures freqs of wake-ups in ACC-only mode and allows to put all 6 axis into standby
MPU_ADDR              = const(0x68)   # The adress of the acceleration sensor itself
SIGNAL_PATHS_RESET    = const(0x68)   # Resets analog and digital signal paths of GYR, ACC & TMP sensors
MOTION_DETECTION      = const(0x69)   # Settings for the motion detection
WHOAMI                = const(0x75)   # I2C Testing


i2c_ = None

def init_sensor(i2c_obj, scl=None, sda=None):
    global i2c_
    i2c_ = i2c_obj
    i2c_.init(scl=scl,sda=sda)
    i2c_.writeto(MPU_ADDR, bytearray([107, 0]))

def sleepmode():
    global i2c_
    i2c_.writeto(MPU_ADDR, bytearray([0x6B, 0x20]))

def wakeup():
    global i2c_
    i2c_.writeto(MPU_ADDR, bytearray([0x6B, 0x00]))  ## Turns the temperature sensor on again, need to be replaced by 0x08

def get_raw_values():
    global i2c_
    a = i2c_.readfrom_mem(MPU_ADDR, 0x3B, 14)
    return a

def get_ints():
    b = get_raw_values()
    c = []
    for i in b:
        c.append(i)
    return c

def bytes_toint(firstbyte, secondbyte):
    if not firstbyte & 0x80:
        return firstbyte << 8 | secondbyte
    return - (((firstbyte ^ 255) << 8) | (secondbyte ^ 255) + 1)

def get_values():
    raw_ints = get_raw_values()
    vals = {}
    vals["AX"] = bytes_toint(raw_ints[0], raw_ints[1])
    vals["AY"] = bytes_toint(raw_ints[2], raw_ints[3])
    vals["AZ"] = bytes_toint(raw_ints[4], raw_ints[5])
    vals["GX"] = bytes_toint(raw_ints[8], raw_ints[9])
    vals["GY"] = bytes_toint(raw_ints[10], raw_ints[11])
    vals["GZ"] = bytes_toint(raw_ints[12], raw_ints[13])
    vals["Tmp"] = bytes_toint(raw_ints[6], raw_ints[7]) / 340.00 + 36.53
    return vals  # returned in range of Int16
    # -32768 to 32767

def val_test():
    while 1:
        print(get_values())
        sleep(0.5)
        
def i2c_test():
    global i2c_
    b = i2c_.readfrom_mem(MPU_ADDR, WHOAMI, 1)
    c = []
    for i in b:
        c.append(i)
    #c = hex(c)
    #c = c
    #c = hex(int(c)).split('x')[-1]
    #b = format(ord("b"), "x")
    #b = bytes_toint(b,b)
    return c


def motion_detect_on():
     global i2c_
#      i2c_.writeto(MPU_ADDR, bytearray([INT_ENABLE, 0x40]))
#      i2c_.writeto(MPU_ADDR, bytearray([MOTION_DURATION, 1]))
#      i2c_.writeto(MPU_ADDR, bytearray([MOTION_THRESHOLD, 20]))  
     print('Printing POWER_MGMT')
     i2c_.writeto(MPU_ADDR, bytearray([POWER_MGMT_1, 0x00]))       # 0x6B
     print('Resetting all signal paths and filters')
     i2c_.writeto(MPU_ADDR, bytearray([SIGNAL_PATHS_RESET, 0x07])) # 0x68
     print('Printing I2C_BYPASS_ENABLE')
     i2c_.writeto(MPU_ADDR, bytearray([I2C_BYPASS_ENABLE, 0xA0]))  # 0x37  vorher 0x20, jetzt A0
     print('Printing ACC_CONFIG')
     i2c_.writeto(MPU_ADDR, bytearray([ACC_CONFIG, 0x01]))         # 0x1C
     print('Setting motion threshold to 20mG')
     i2c_.writeto(MPU_ADDR, bytearray([MOTION_THRESHOLD, 20]))     # 0x1F
     print('Setting motion duration to 20ms')
     i2c_.writeto(MPU_ADDR, bytearray([MOTION_DURATION, 20]))      # 0x20
     print('Printing MOTION_DETECTION')
     i2c_.writeto(MPU_ADDR, bytearray([MOTION_DETECTION, 0x15]))   # 0x69
     print('Printing INT_ENABLE')
     i2c_.writeto(MPU_ADDR, bytearray([INT_ENABLE, 0x40]))         # 0x38
    
def get_interrupt_status():
    global i2c_
    a = i2c_.readfrom_mem(MPU_ADDR, INT_STATUS, 1) # 0x3A
    return a

def turnoff_temp_sensor():
    global i2c_
    i2c_.writeto(MPU_ADDR, bytearray([POWER_MGMT_1, 0x08]))

def turnon_temp_sensor():
    global i2c_
    i2c_.writeto(MPU_ADDR, bytearray([POWER_MGMT_1, 0x00]))

def turnoff_gyro():
    global i2c_
    i2c_.writeto(MPU_ADDR, bytearray([POWER_MGMT_2, 0x07]))
    
def turnon_gyro():
    global i2c_
    i2c_.writeto(MPU_ADDR, bytearray([POWER_MGMT_2, 0x00]))
    
def read_reg(REG_ADDR):
    global i2c_
    a = i2c_.readfrom_mem(MPU_ADDR, REG_ADDR, 1)
    print(a)
    
def write_reg(REG_ADDR, HEX):
    global i2c_
    i2c_.writeto(MPU_ADDR, bytearray([REG_ADDR, HEX]))
    print("%s written to %s" % (HEX, REG_ADDR))
    
    