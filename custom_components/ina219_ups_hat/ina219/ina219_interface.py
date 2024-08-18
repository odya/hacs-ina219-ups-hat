from abc import ABC, abstractmethod


# Define the interface for INA219
class INA219Interface(ABC):
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
