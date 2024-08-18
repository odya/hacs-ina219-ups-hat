"""Constants."""

MIN_BATTERY_CONNECTED_CURRENT = 0.1
LOW_BATTERY_PERCENTAGE = 20
DEFAULT_OCV = {
    0: 2.5,
    10: 3.0,
    20: 3.2,
    30: 3.4,
    40: 3.5,
    50: 3.6,
    60: 3.7,
    70: 3.8,
    80: 3.9,
    90: 4.0,
    100: 4.2,
}

DOMAIN = "ina219_ups_hat"
DEFAULT_UNIQUE_ID = "hassio_ups"
DEFAULT_NAME = "Hassio UPS"

CONF_BATTERY_CAPACITY = "battery_capacity"
CONF_ADDR = "addr"
CONF_MAX_SOC = "max_soc"
CONF_SMA_SAMPLES = "sma_samples"
CONF_MIN_ONLINE_CURRENT = "min_online_current"
CONF_MIN_CHARGING_CURRENT = "min_charging_current"
CONF_BATTERIES_COUNT = "batteries_count"
CONF_SCAN_INTERVAL = "scan_interval"

ATTR_CAPACITY = "capacity"
ATTR_SOC = "soc"
ATTR_REAL_SOC = "real_soc"
ATTR_PSU_VOLTAGE = "psu_voltage"
ATTR_SHUNT_VOLTAGE = "shunt_voltage"
ATTR_LOAD_VOLTAGE = "load_voltage"
ATTR_CURRENT = "current"
ATTR_POWER = "power"
ATTR_CHARGING = "charging"
ATTR_ONLINE = "online"
ATTR_BATTERY_CONNECTED = "battery_connected"
ATTR_LOW_BATTERY = "low_battery"
ATTR_POWER_CALCULATED = "power_calculated"
ATTR_REMAINING_BATTERY_CAPACITY = "remaining_battery_capacity"
ATTR_REMAINING_TIME = "remaining_time_min"
