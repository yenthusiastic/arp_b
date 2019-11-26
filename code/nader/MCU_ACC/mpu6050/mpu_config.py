# Registers
WHOAMI                = const(0x75)   #I2C Testing
MPU_ADDR              = const(0x68)   #
SIGNAL_PATHS_RESET    = const(0x68)   #Resets analog and digital signal paths of GYR, ACC & TMP sensors
I2C_BYPASS_ENABLE     = const(0x37)   #Configures the behaviour of the interrupt signal at the INT pins
ACC_CONFIG            = const(0x1C)   #
MOTION_THRESHOLD      = const(0x1F)   #
MOTION_DURATION       = const(0x20)   #
MOTION_DETECTION      = const(0x69)   #
INT_ENABLE            = const(0x38)   #
INT_STATUS            = const(0x3A)   #

i2c_ = None

def i2c_test():
    global i2c_
    i = i2c_.readfrom_mem(MPU_ADDR, WHOAMI, 1)
    return i