

addr=0x68

i2c_ = None

def init_sensor(i2c_obj, scl=None, sda=None):
    global i2c_
    i2c_ = i2c_obj
    i2c_.init(scl=scl,sda=sda)
    i2c_.writeto(addr, bytearray([107, 0]))

def sleepmode():
    global i2c_
    i2c_.writeto(addr, bytearray([0x6B, 0x20]))

def wakeup():
    global i2c_
    i2c_.writeto(addr, bytearray([0x6B, 0x00]))

def get_raw_values():
    global i2c_
    a = i2c_.readfrom_mem(addr, 0x3B, 14)
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
