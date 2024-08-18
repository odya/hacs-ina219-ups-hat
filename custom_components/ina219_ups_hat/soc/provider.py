import numpy as np
import pandas as pd
from scipy.interpolate import interp1d
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
        cubic_interp_func = interp1d(
            soc_voltage_df["SOC"],
            soc_voltage_df["Voltage"],
            kind="cubic",
            fill_value="extrapolate",
        )
        # Precalculate detailed SOC-Voltage data
        detailed_soc = np.linspace(0, 100, 100)
        detailed_voltage = cubic_interp_func(detailed_soc)
        # Create a new DataFrame for the detailed SOC-Voltage data
        self._detailed_soc_voltage_df = pd.DataFrame(
            {"SOC": detailed_soc, "Voltage": detailed_voltage}
        )

        # Interpolation function
        self._linear_interp_func = interp1d(
            self._detailed_soc_voltage_df["Voltage"],
            self._detailed_soc_voltage_df["SOC"],
            kind="linear",
            fill_value="extrapolate",
        )

    def get_soc_from_voltage(self, cell_voltage: float) -> float:
        # Ensure the voltage is within the measurable range
        if cell_voltage > self._detailed_soc_voltage_df["Voltage"].max():
            return 100
        if cell_voltage < self._detailed_soc_voltage_df["Voltage"].min():
            return 0

        # Interpolate the SOC based on the voltage
        return float(self._linear_interp_func(cell_voltage))
