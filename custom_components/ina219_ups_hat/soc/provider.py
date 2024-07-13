import json
import os
import numpy as np
import pandas as pd
from scipy.interpolate import interp1d


class SocOcvProvider():
    def __init__(self, ocv_file) -> None:
        """Initialize SocOcvProvider"""

        current_file_path = os.path.dirname(__file__)
        current_dir = os.path.abspath(os.path.join(current_file_path, '.'))
        soc_voltage_data = self.load_json_to_dict(os.path.join(current_dir, ocv_file))

        soc_voltage_df = pd.DataFrame(list(soc_voltage_data.items()), columns=['SOC', 'Voltage'])
        # print(soc_voltage_df)

        # Create the cubic interpolation function
        cubic_interp_func = interp1d(soc_voltage_df['SOC'], soc_voltage_df['Voltage'],
                                    kind='cubic', fill_value="extrapolate")
        # Precalculate detailed SOC-Voltage data
        detailed_soc = np.linspace(0, 100, 100)
        detailed_voltage = cubic_interp_func(detailed_soc)
        # Create a new DataFrame for the detailed SOC-Voltage data
        self._detailed_soc_voltage_df = pd.DataFrame(
            {'SOC': detailed_soc, 'Voltage': detailed_voltage})
        # print(self._detailed_soc_voltage_df)

        # Interpolation function
        self._linear_interp_func = interp1d(
            self._detailed_soc_voltage_df['Voltage'], self._detailed_soc_voltage_df['SOC'], kind='linear', fill_value="extrapolate")


    def load_json_to_dict(self, ocv_file_path):
        with open(ocv_file_path, 'r') as file:
            data = json.load(file)
        data_dict = {float(key): float(value) for key, value in data.items()}
        data_dict = {k: data_dict[k]
                    for k in sorted(data_dict.keys(), reverse=False)}
        return data_dict

    def get_soc_from_voltage(self, cell_voltage: float) -> float:
        df = self._detailed_soc_voltage_df

        # Ensure the voltage is within the measurable range
        if cell_voltage > df['Voltage'].max():
            return 100
        elif cell_voltage < df['Voltage'].min():
            return 0

        # Interpolate the SOC based on the voltage
        soc = float(self._linear_interp_func(cell_voltage))
        return soc