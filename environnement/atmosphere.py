# Atmosphere class
# The model is based on the International Standard Atmosphere (ISA) model
# All information available on wikipedia:
# - https://en.wikipedia.org/wiki/Barometric_formula
# - https://fr.wikipedia.org/wiki/Formule_du_nivellement_barom%C3%A9trique (évolution de température linéaire) 
# - https://en.wikipedia.org/wiki/International_Standard_Atmosphere
import numpy as np
import matplotlib.pyplot as plt

class AtmosphereISA:
    def __init__(self) -> None:
        pass

    # Get the atmosphere level according to the ISA standard
    def get_level(self, height):
        if height < 11000:  # Troposphere
            return 0
        elif height < 20000: # Tropopause
            return 1
        elif height < 32000: # Stratosphere
            return 2
        elif height < 47000: # Stratopause
            return 3
        elif height < 51000: # Mesosphere
            return 4
        elif height < 71000: # Mesopause
            return 5

    # Get the temperature at a given height
    def get_temperature(self, height) -> float:
        _level = self.get_level(height)
        _Tb = [288.15, 216.65, 216.65, 228.65, 270.65, 270.65][_level]
        _a = [-0.0065, 0, 0.001, 0.0028, 0, -0.0028][_level]
        _hb = [0, 11000, 20000, 32000, 47000, 51000][_level]
        return _Tb + _a * (height - _hb)

    # Get the pressure at a given height
    def get_pressure(self, height) -> float:
        _level = self.get_level(height)
        _Pb = [101325.00, 22632.06, 5474.89, 868.02, 110.91, 66.94][_level]
        _Tb = [288.15, 216.65, 216.65, 228.65, 270.65, 270.65][_level]
        _Lb = [0.0065, 0, -0.001, -0.0028, 0, 0.0028][_level]
        _hb = [0, 11000, 20000, 32000, 47000, 51000][_level]
        if _Lb == 0:
            return _Pb * np.exp(-9.81 * 0.028964 * (height - _hb) / (8.314 * _Tb))
        else:
            return _Pb * (1 - _Lb * (height - _hb) / _Tb) ** (9.81 * 0.028964/ (8.314 * _Lb))

    # Get the density at a given height
    def get_density(self, height) -> float:
        _level = self.get_level(height)
        _Db = [1.225, 0.36391, 0.08803, 0.01322, 0.00143, 0.00086][_level]
        _Tb = [288.15, 216.65, 216.65, 228.65, 270.65, 270.65][_level]
        _Lb = [0.0065, 0, -0.001, -0.0028, 0, 0.0028][_level]
        _hb = [0, 11000, 20000, 32000, 47000, 51000][_level]
        if _Lb == 0:
            return _Db * np.exp(-9.81 * 0.028964 * (height - _hb) / (8.314 * _Tb))
        else:
            return _Db * (1 - _Lb * (height - _hb) / _Tb) ** (9.81 * 0.028964/ (8.314 * _Lb) - 1)

if __name__ == '__main__':
    atm = AtmosphereISA()

    # Generate altitude data
    altitude_data = np.arange(0, 40001, 100)

    # Generate temperature data
    temperature_data = [atm.get_temperature(alt) for alt in altitude_data]

    # Generate pressure data
    pressure_data = [atm.get_pressure(alt) for alt in altitude_data]

    # Generate density data
    density_data = [atm.get_density(alt) for alt in altitude_data]

    # Plot temperature
    plt.plot(altitude_data, temperature_data)
    plt.xlabel('Altitude (m)')
    plt.ylabel('Temperature (K)')
    plt.title('Temperature Evolution with Altitude')
    plt.show()

    # Plot pressure
    plt.plot(altitude_data, pressure_data)
    plt.xlabel('Altitude (m)')
    plt.ylabel('Pressure (Pa)')
    plt.title('Pressure Evolution with Altitude')
    plt.show()

    # Plot density
    plt.plot(altitude_data, density_data)
    plt.xlabel('Altitude (m)')
    plt.ylabel('Density (kg/m^3)')
    plt.title('Density Evolution with Altitude')
    plt.show()