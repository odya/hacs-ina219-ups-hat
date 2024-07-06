from abc import ABC, abstractmethod

# Define the interface for INA219
class INA219Interface(ABC):
    @abstractmethod
    def read(self, address):
        pass

    @abstractmethod
    def write(self, address, data):
        pass

    @abstractmethod
    def set_calibration_32V_2A(self):
        pass

    @abstractmethod
    def getShuntVoltage_mV(self):
        pass

    @abstractmethod
    def getBusVoltage_V(self):
        pass

    @abstractmethod
    def getCurrent_mA(self):
        pass

    @abstractmethod
    def getPower_W(self):
        pass
