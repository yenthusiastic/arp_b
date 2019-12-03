import time

# Acceleration registers
_REG_WHOAMI                = const(0x0F)   # Who am I (0x33)
_REG_TEMPCFG               = const(0x1F)
_REG_ACC_CONFIG            = const(0x20)   # Axis configurations and power-modes
_REG_HIGH_PASS_FILTER      = const(0x21)   # Configuring the high-pass filters
_REG_INT_CONFIG            = const(0x22)   # Interrupt configurations
_REG_SCALE_MODES           = const(0x23)   # Set-up the full-scale of the accelerometer
_REG_LATCH_CONFIG          = const(0x24)   # Latch configurations
_REG_INT_LOGICS            = const(0x30)   # Interrupt configurations (different axis)
_REG_INTERRUPT             = const(0x31)   # Interrupt status
_REG_THRESHOLD             = const(0x32)   # Acceleration threshold
_REG_DURATION              = const(0x33)   # Acceleration duration

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
    write_reg(_REG_LATCH_CONFIG, 0x80)
    time.sleep(0.01)
    write_reg(_REG_ACC_CONFIG, 0x07)
    write_reg(_REG_SCALE_MODES, 0x88)
    write_reg(_REG_TEMPCFG, 0x80)
    write_reg(_REG_LATCH_CONFIG, 0x08)


def acceleration():
    """
    
    The x, y, z acceleration values returned in a 3-tuple and are in m / s ^ 2.
    
    """
    divider = 1

    #x, y, z = struct.unpack('<hhh', self._read_register(_REG_OUT_X_L | 0x80, 6))

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
    b = i2c_.readfrom_mem(IMU_ADDRESS, _REG_WHOAMI, 1)
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
    i2c_.writeto(IMU_ADDRESS, bytearray([REG_ADDR, HEX]))
    print("%s written to %s" % (HEX, REG_ADDR))
    

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
    i2c_.writeto(IMU_ADDRESS, bytearray([_REG_DURATION, DURATION]))


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
    i2c_.writeto(IMU_ADDRESS, bytearray([_REG_THRESHOLD, THRESHOLD]))


def set_interrupts(DURATION, THRESHOLD):
    """

    Here, all the parameters necessary for an appropriate interrupt are defined and written into the registers of the accelerometer.

    :variable _REG_HIGH_PASS_FILTER (0x21): Used to activate the inbuilt High-Pass Filter
    :variable _REG_INT_CONFIG (0x22): Enables the general interrupt(s)
    :variable _REG_SCALE_MODES (0x23): Defines the scale of the acceleration sensor (±2G, ±4G, ±8G, ±16G)
    :variable _REG_LATCH_CONFIG (0x24): Activating latched interrupt requests
    :variable _REG_THRESHOLD (0x32): Defines the interrupt threshold value
    :variable _REG_DURATION (0x33): Defines the interrupt duration of the interrupt event
    :variable _REG_INT_LOGICS (0x30): Enabling interrupt generations on all axis with a logical OR-Combination of interrupt events
    :variable _REG_ACC_CONFIG (0x20): Activating all three axis including Low-Power mode (ODR of 100Hz) 

    """
    global i2c_
    print('Writing to registers...')
    i2c_.writeto(IMU_ADDRESS, bytearray([_REG_HIGH_PASS_FILTER, 0x09]))
    i2c_.writeto(IMU_ADDRESS, bytearray([_REG_INT_CONFIG, 0x40]))
    i2c_.writeto(IMU_ADDRESS, bytearray([_REG_SCALE_MODES, 0x00]))
    i2c_.writeto(IMU_ADDRESS, bytearray([_REG_LATCH_CONFIG, 0x00]))
    i2c_.writeto(IMU_ADDRESS, bytearray([_REG_THRESHOLD, 0x06]))
    i2c_.writeto(IMU_ADDRESS, bytearray([_REG_DURATION, 0x00]))
    i2c_.writeto(IMU_ADDRESS, bytearray([_REG_INT_LOGICS, 0x2A]))
    i2c_.writeto(IMU_ADDRESS, bytearray([_REG_ACC_CONFIG, 0x5F]))
    print('Writing completed!')
    
    
