import numpy as np
import pandas as pd

from homeassistant import core


class SocOcvProvider:
    def __init__(self, hass: core.HomeAssistant, ocv_map) -> None:
        """Initialize SocOcvProvider."""

        self._hass = hass
        soc_voltage_data = ocv_map

        soc_voltage_df = pd.DataFrame(
            list(soc_voltage_data.items()), columns=["SOC", "Voltage"]
        )

        # Create the cubic interpolation function
        coefficients = np.polyfit(soc_voltage_df["SOC"], soc_voltage_df["Voltage"], 3)
        cubic_interp_func = np.poly1d(coefficients)
        # Precalculate detailed SOC-Voltage data
        detailed_soc = np.linspace(0, 100, 100)
        detailed_voltage = cubic_interp_func(detailed_soc)
        # Create a new DataFrame for the detailed SOC-Voltage data
        self._detailed_soc_voltage_df = pd.DataFrame(
            {"SOC": detailed_soc, "Voltage": detailed_voltage}
        )

    def get_soc_from_voltage(self, cell_voltage: float) -> float:
        # Ensure the voltage is within the measurable range
        if cell_voltage >= self._detailed_soc_voltage_df["Voltage"].max():
            return 100
        if cell_voltage <= self._detailed_soc_voltage_df["Voltage"].min():
            return 0

        # Interpolate the SOC based on the voltage
        return float(
            np.interp(
                cell_voltage,
                self._detailed_soc_voltage_df["Voltage"],
                self._detailed_soc_voltage_df["SOC"],
            )
        )
