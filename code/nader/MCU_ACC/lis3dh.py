import time

# Acceleration registers
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

# Register constants:
RANGE_16_G                 = const(0b11)   # +/- 16g
RANGE_8_G                  = const(0b10)   # +/- 8g
RANGE_4_G                  = const(0b01)   # +/- 4g
RANGE_2_G                  = const(0b00)   # +/- 2g (default)

# Other variables
IMU_ADDRESS                = const(0x18)
INTERRUPT_PIN              = 27
reading                    = 0
interruptFlag              = False


i2c_ = None


def init_sensor(i2c_obj, scl=None, sda=None):
    """

    This function is used to intitiate the I2C-Communication between the acceleration sensor and microcontroller.

    """
    global i2c_
    i2c_ = i2c_obj
    i2c_.init(scl=scl,sda=sda)
    
    
def init_me():
    write_reg(REG_LATCH_CONFIG, b'\x08')
    time.sleep(0.01)
    write_reg(REG_ACC_CONFIG, b'\x07')
    write_reg(REG_SCALE_MODES, b'\x88')
    write_reg(REG_TEMPCFG, b'\x80')
    write_reg(REG_LATCH_CONFIG, b'\x08')


def acceleration():
    """
    
    The x, y, z acceleration values returned in a 3-tuple and are in m / s ^ 2.
    
    """
    divider = 1

    #x, y, z = struct.unpack('<hhh', self._read_register(REG_OUT_X_L | 0x80, 6))

    x = read_reg(0x28)
    y = read_reg(0x2A)
    z = read_reg(0x2C)

    # convert from Gs to m / s ^ 2 and adjust for the range
    #x = (x / divider) * 9.81
    #y = (y / divider) * 9.81
    #z = (z / divider) * 9.81

    return x, y, z


def i2c_test():
    """

    Used in order to test the I2C-Communication. Output should be 51 (or 0x33).
    
    """
    global i2c_
    b = i2c_.readfrom_mem(IMU_ADDRESS, REG_WHOAMI, 1)
    c = []
    for i in b:
        c.append(i)
    return c


def read_reg(REG_ADDR):
    """

    Reads and prints any desired register (for debugging purposes)

    :params REG_ADDR:   Register of the acceleration sensor, which the users wants to read.

    """
    global i2c_
    a = i2c_.readfrom_mem(IMU_ADDRESS, REG_ADDR, 1)
    print(a)
    

def write_reg(REG_ADDR, HEX):
    """

    Writes any data to any arbitrary register.

    :param REG_ADDR:    Defines the address of the register, where the data is written to (e.g. )

    :param HEX:         Here the data is defined, which is written to the chosen register

    """
    global i2c_
    i2c_.writeto_mem(IMU_ADDRESS, REG_ADDR, DATA)
    print("%s written to address %s" % (DATA, REG_ADDR))
    

def set_duration(TIME_IN_MS):
    """

    Sets the minimum duration for the interrupt event to be recognized into the register of the accelerometer.
    The duration steps and maximum values depend on the ODR, which had been chosen. (compare _REG_ACC_CONFIG).
    The duration is calculated with N/ODR, where N is 'TIME'IN MS/10'.

    :param TIME_IN_MS:  The desired duration of the interrupt event in milliseconds.

    """
    global i2c_
    DURATION = TIME_IN_MS/10
    DURATION = round(DURATION)
    DURATION = bytearray(DURATION)
    write_reg(REG_DURATION, DURATION)


def set_threshold(THRESHOLD_IN_MG, RANGE):
    """

    Sets the maximum or minimum threshold of the interrupt event to be recognized. The threshold is then written into 
    the appropriate register.  

    :param THRESHOLD_IN_MG: The desired threshold of the interrupt event in milli g (acceleration force).

    :param RANGE:           The range of the accelerometer in milli g, which is set in the register _REG_SCALE_MODES (default 16000)

    """
    global i2c_
    THRESHOLD = THRESHOLD_IN_MG/(RANGE/128)
    THRESHOLD = round(THRESHOLD)
    THRESHOLD = hex(THRESHOLD)
    THRESHOLD = bytearray([THRESHOLD])
    write_reg(REG_THRESHOLD, THRESHOLD)


def set_interrupts(DURATION, THRESHOLD):
    """

    Here, all the parameters necessary for an appropriate interrupt are defined and written into the registers of the accelerometer.

    :variable REG_HIGH_PASS_FILTER (0x21): Used to activate the inbuilt High-Pass Filter
    :variable REG_INT_CONFIG (0x22): Enables the general interrupt(s)
    :variable REG_SCALE_MODES (0x23): Defines the scale of the acceleration sensor (±2G, ±4G, ±8G, ±16G)
    :variable REG_LATCH_CONFIG (0x24): Activating latched interrupt requests
    :variable REG_THRESHOLD (0x32): Defines the interrupt threshold value
    :variable REG_DURATION (0x33): Defines the interrupt duration of the interrupt event
    :variable REG_INT_LOGICS (0x30): Enabling interrupt generations on all axis with a logical OR-Combination of interrupt events
    :variable REG_ACC_CONFIG (0x20): Activating all three axis including Low-Power mode (ODR of 100Hz) 

    """
    global i2c_
    print('Writing to registers...')
    write_reg(REG_HIGH_PASS_FILTER, b'\x09')
    write_reg(REG_INT_CONFIG, b'\x40')
    write_reg(REG_SCALE_MODES, b'\x00')
    write_reg(REG_LATCH_CONFIG, b'\x00')
    write_reg(REG_THRESHOLD, HEb'\x06'X)
    write_reg(REG_DURATION, b'\x00')
    write_reg(REG_INT_LOGICS, b'\x2A')
    write_reg(REG_ACC_CONFIG, b'\x5F')
    print('Writing completed!')
    
    
