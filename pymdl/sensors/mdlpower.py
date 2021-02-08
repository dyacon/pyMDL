'''
A sensor to import mdl power values into the data table
Measure's mdl power system values
'''

import datetime
import time
from databear.errors import MeasureError, SensorConfigError
from databear.sensors import sensor

class mdlpower(sensor.Sensor):
    points = [ '3x3Ext', '5V', '12V', '3x3Int']
    measurements = []
    measurement_description = {}
    units = {}
    
    for i in range(4): 
        point = points[i]
        measurements.append(point + "Volts")
        measurements.append(point + "Current")
        measurements.append(point + "Power")
        measurements.append(point + "Energy")

        measurement_description[point + "Volts"] = point + " Voltage"
        measurement_description[point + "Current"] = point + " Current"
        measurement_description[point + "Power"] = point + " Power"
        measurement_description[point + "Energy"] = point + " Energy"

        units[point + "Volts"] = "v"
        units[point + "Current"] = "mA"
        units[point + "Power"] = "mW"
        units[point + "Energy"] = ""

    def __init__(self,name,sn,address):
        '''
        Create a new simulator
        - Call base class init
        - Override base data structure
        '''
        super().__init__(name,sn,address)

        self.devicePath = '/sys/bus/iio/devices/iio:device0'
        self.in_voltage_scale = self.numberFromFile(self.devicePath + '/in_voltage_scale')

    def numberFromFile(self, filename):
        number = -1
        with open(filename) as f:
            number = float(f.read())
        return number

    def measure(self):
        '''
        Override base method
        - Load data from device
        '''

        dt = datetime.datetime.now()

        # Measure the data from the /sys device

        for i in range(4):
            # string representation of i
            istring = str(i)

            # First read in each scale
            vadc = self.numberFromFile(self.devicePath + '/in_voltage' + istring + '_mean_raw')
            cadc = self.numberFromFile(self.devicePath + '/in_current' + istring + '_mean_raw')
            padc = self.numberFromFile(self.devicePath + '/in_power' + istring + '_raw')
            eadc = self.numberFromFile(self.devicePath + '/in_energy' + istring + '_mean_raw')

            # Next read scales
            currentScale = self.numberFromFile(self.devicePath + '/in_current' + istring + '_scale')
            powerScale = self.numberFromFile(self.devicePath + '/in_power' + istring + '_scale')
            energyScale = self.numberFromFile(self.devicePath + '/in_energy' + istring + '_scale')

            volts = (vadc * self.in_voltage_scale) / 1000
            current = (cadc * currentScale)
            power = (padc * powerScale) / 1000
            energy = (eadc * energyScale)

            self.data[self.points[i] + "Volts"].append((dt, volts))
            self.data[self.points[i] + "Current"].append((dt, current))
            self.data[self.points[i] + "Power"].append((dt, power))
            self.data[self.points[i] + "Energy"].append((dt, energy))

