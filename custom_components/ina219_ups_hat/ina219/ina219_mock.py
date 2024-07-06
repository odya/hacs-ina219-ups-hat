from .ina219_interface import INA219Interface


class MockSMBus:
    def __init__(self, bus):
        self.regs = {}
        self.addr = None

    def read_i2c_block_data(self, addr, reg, length):
        self.addr = addr
        return [(self.regs.get(reg, 0) >> 8) & 0xFF, self.regs.get(reg, 0) & 0xFF]

    def write_i2c_block_data(self, addr, reg, data):
        self.addr = addr
        self.regs[reg] = (data[0] << 8) | data[1]

# Constants
_REG_CONFIG = 0x00
_REG_SHUNTVOLTAGE = 0x01
_REG_BUSVOLTAGE = 0x02
_REG_POWER = 0x03
_REG_CURRENT = 0x04
_REG_CALIBRATION = 0x05

class MockINA219(INA219Interface):
    def __init__(self, i2c_bus=1, addr=0x40):
        self.bus = MockSMBus(i2c_bus)
        self.addr = addr
        self._cal_value = 0
        self._current_lsb = 0
        self._power_lsb = 0
        self.set_calibration_32V_2A()

    def read(self, address):
        data = self.bus.read_i2c_block_data(self.addr, address, 2)
        return (data[0] << 8) + data[1]

    def write(self, address, data):
        self.bus.write_i2c_block_data(self.addr, address, [(data >> 8) & 0xFF, data & 0xFF])

    def set_calibration_32V_2A(self):
        self._current_lsb = 0.1
        self._cal_value = 4096
        self._power_lsb = 0.002
        self.write(_REG_CALIBRATION, self._cal_value)
        self.config = 0x399F  # example config value
        self.write(_REG_CONFIG, self.config)

    def getShuntVoltage_mV(self):
        value = self.read(_REG_SHUNTVOLTAGE)
        if value > 32767:
            value -= 65535
        return value * 0.01

    def getBusVoltage_V(self):
        value = self.read(_REG_BUSVOLTAGE)
        return (value >> 3) * 0.004

    def getCurrent_mA(self):
        value = self.read(_REG_CURRENT)
        if value > 32767:
            value -= 65535
        return value * self._current_lsb

    def getPower_W(self):
        value = self.read(_REG_POWER)
        if value > 32767:
            value -= 65535
        return value * self._power_lsb
