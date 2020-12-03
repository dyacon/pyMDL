'''
A sensor to import mdl power values into the data table
Measure's mdl power system values
'''

import datetime
import time
from databear.errors import MeasureError, SensorConfigError
from databear.sensors import sensor

class mdlpower(sensor.Sensor):
    measurements = ['volts0','current0','power0', 'energy0',
            'volts1','current1','power1', 'energy1',
            'volts2','current2','power2', 'energy2',
            'volts3','current3','power3', 'energy3']
    measurement_description = {
        'volts0':'',
        'volts1':'',
        'volts2':'',
        'volts3':'',
        'current0':'',
        'current1':'',
        'current2':'',
        'current3':'',
        'power0':'',
        'power1':'',
        'power2':'',
        'power3':'',
        'energy0':'',
        'energy1':'',
        'energy2':'',
        'energy3':''
    } 
    units = {
        'volts0':'v',
        'volts1':'v',
        'volts2':'v',
        'volts3':'v',
        'current0':'mA',
        'current1':'mA',
        'current2':'mA',
        'current3':'mA',
        'power0':'mW',
        'power1':'mW',
        'power2':'mW',
        'power3':'mW',
        'energy0':'',
        'energy1':'',
        'energy2':'',
        'energy3':''
    }

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

        for i in range(3):
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

            self.data['volts' + istring].append((dt, volts))
            self.data['current' + istring].append((dt, current))
            self.data['power' + istring].append((dt, power))
            self.data['energy' + istring].append((dt, energy))

