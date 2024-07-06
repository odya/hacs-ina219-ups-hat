import os
from .ina219 import INA219
from .ina219_mock import MockINA219

def get_ina219_class():
    if os.getenv('ENV') == 'dev':
        return MockINA219
    return INA219