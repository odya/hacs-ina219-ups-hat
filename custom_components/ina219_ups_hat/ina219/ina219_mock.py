import random

from .ina219_interface import INA219Interface


class MockINA219(INA219Interface):
    def __init__(self, i2c_bus=1, addr=0x40):
        print(i2c_bus, addr)

    def getShuntVoltage_mV(self):
        value = random.randint(20, 200)
        return value
        value = random.randint(20, 200)
        return value

    def getBusVoltage_V(self):
        value = random.randint(900, 1243)
        return value * 0.01
        value = random.randint(900, 1243)
        return value * 0.01

    def getCurrent_mA(self):
        value = random.randint(-500, 1500)
        return value
        value = random.randint(-500, 1500)
        return value

    def getPower_W(self):
        value = random.randint(-4, 15)
        return value
        value = random.randint(-4, 15)
        return value
