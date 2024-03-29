'''
A driver for Databear on the MDL
'''
from pymdl.utilities import gpioconfig

class dbdriver:
    def __init__(self):
        '''
        Create a new driver instance
        Could load a config file here...
        '''
        #Map DataBear ports to hardware ports
        self.ports = {
            'port0':'',
            'port1':'/dev/ttyMAX0',
            'port2':'/dev/ttyMAX1',
            'port3':'/dev/ttyMAX2',
            'port4':'/dev/ttyMAX3',
            'port5':'/dev/ttyMAX4',
            'port6':'/dev/ttyMAX5',
            'port7':'/dev/ttyMAX6',
            'port8':'/dev/ttyMAX7',
            'busport1':'/dev/ttyMAX0'
        }
    def connect(self,databearport,sensor_settings):
        '''
        Configure hardware port and return name
        '''
        mdlport = self.ports[databearport]

        #Only configure GPIO if not port0 (internal/simulated sensors)
        if databearport != 'port0':
            gpioconfig(
                mdlport,
                sensor_settings['serial'],
                sensor_settings['duplex'],
                sensor_settings['resistors'],
                sensor_settings['bias'])

        return mdlport

